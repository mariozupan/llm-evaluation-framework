
import ast
import json
import re
from json import JSONDecoder
from typing import Dict, List, Any, Optional

import datasets


# ---------- parsing helpers ----------

def _unwrap_tuple_wrapped_text(s: str) -> str:
    s = (s or "").strip()
    try:
        v = ast.literal_eval(s)
        if isinstance(v, tuple) and len(v) == 1 and isinstance(v[0], str):
            return v[0]
    except Exception:
        pass
    return s


def _to_float(x: Any) -> Optional[float]:
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, str):
        s = x.strip().replace(" ", "")
        # decimal comma "123,45"
        if re.match(r"^-?\d+,\d+$", s):
            s = s.replace(",", ".")
        try:
            return float(s.replace(",", ""))  # tolerate thousands separators
        except Exception:
            return None
    return None


def _normalize_account_class(acc: Any) -> str:
    """
    Account class = first 2 digits of account number.
    Examples:
      "14" == "14000" == "140000" -> "14"
      "6630" -> "66"
      "029-001" -> digits "029001" -> "02"
    """
    if acc is None:
        return ""
    digits = re.sub(r"\D", "", str(acc))
    if len(digits) >= 2:
        return digits[:2]
    return digits


def _side_mask(debit_val: Any, credit_val: Any, side_zero_tol: float = 1e-6) -> int:
    """1 = debit used, 2 = credit used, 3 = both"""
    d = _to_float(debit_val)
    c = _to_float(credit_val)
    used_d = (d is not None) and (abs(d) > side_zero_tol)
    used_c = (c is not None) and (abs(c) > side_zero_tol)
    return (1 if used_d else 0) | (2 if used_c else 0)


def _extract_first_json_object(text: str) -> Optional[dict]:
    """
    Find the first JSON object anywhere in text.
    Avoids greedy regex issues with extra braces later (e.g. \\boxed{...}).
    """
    if not text:
        return None
    s = text.strip()

    try:
        obj = json.loads(s)
        return obj if isinstance(obj, dict) else None
    except Exception:
        pass

    dec = JSONDecoder()
    for m in re.finditer(r"\{", s):
        i = m.start()
        try:
            obj, _end = dec.raw_decode(s[i:])
            if isinstance(obj, dict):
                return obj
        except Exception:
            continue
    return None


def _entries_from_obj(obj: dict) -> List[dict]:
    entries = obj.get("entries")
    if isinstance(entries, list):
        return [e for e in entries if isinstance(e, dict)]
    return []


def _extract_entries_from_text(text: str) -> List[dict]:
    """
    1) JSON object anywhere -> entries
    2) fallback bullet/line: "Debit ... account: 140000: 1,500.00"
    """
    obj = _extract_first_json_object(text)
    if isinstance(obj, dict):
        ents = _entries_from_obj(obj)
        if ents:
            return ents

    patt = re.compile(
        r"\b(Debit|Credit)\b.*?account\s*[:=]\s*([0-9][0-9A-Za-z\-]*)\s*\)?\s*[:\-]\s*([-+]?\d[\d\., ]*)",
        flags=re.IGNORECASE | re.DOTALL,
    )

    entries: List[dict] = []
    for m in patt.finditer(text or ""):
        side = m.group(1).lower()
        acc = m.group(2)
        amt = _to_float(m.group(3))
        if amt is None:
            continue
        if side == "debit":
            entries.append({"ACCOUNT": acc, "DEBIT": amt, "CREDIT": 0.0})
        else:
            entries.append({"ACCOUNT": acc, "DEBIT": 0.0, "CREDIT": amt})

    return entries


# ---------- scoring helpers ----------

def _class_side_map_from_entries(entries: List[dict], side_zero_tol: float = 1e-6) -> Dict[str, int]:
    """Aggregate side masks by account class; OR masks inside each class."""
    out: Dict[str, int] = {}
    for e in entries:
        cls = _normalize_account_class(e.get("ACCOUNT", ""))
        if not cls:
            continue
        mask = _side_mask(e.get("DEBIT"), e.get("CREDIT"), side_zero_tol=side_zero_tol)
        if mask == 0:
            continue
        out[cls] = out.get(cls, 0) | mask
    return out


def _balanced_from_entries(entries: List[dict], tol: float = 1e-2) -> bool:
    """Balanced if sum(DEBIT) ~= sum(CREDIT) within tol."""
    if not entries:
        return False
    sd = 0.0
    sc = 0.0
    for e in entries:
        d = _to_float(e.get("DEBIT"))
        c = _to_float(e.get("CREDIT"))
        if d is None or c is None:
            return False
        sd += d
        sc += c
    return abs(sd - sc) <= tol


def _required_list_from_gold(gold_obj: dict, side_zero_tol: float = 1e-6) -> List[dict]:
    """
    Stable schema list: [{"account_class": "66", "side_mask": 3}, ...]
    derived from gold entries.
    """
    gold_entries = _entries_from_obj(gold_obj)
    req_map = _class_side_map_from_entries(gold_entries, side_zero_tol=side_zero_tol)
    return [{"account_class": k, "side_mask": int(v)} for k, v in sorted(req_map.items())]


def _accounts_correct(pred_entries: List[dict], required_list: List[dict], side_zero_tol: float = 1e-6) -> bool:
    """
    For each required class, at least the required side(s) should be used.
    When side_mask=1, debit should be used.
    When side_mask=2, credit should be used.
    When side_mask=3, at least one side should be used.
    """
    pred_map = _class_side_map_from_entries(pred_entries, side_zero_tol=side_zero_tol)

    for item in (required_list or []):
        cls = str(item.get("account_class", "")).strip()
        req = int(item.get("side_mask", 0))
        if not cls or req == 0:
            continue
        pm = int(pred_map.get(cls, 0))

        # The flexible logic:
        # req==1: must have debit (pm & 1) > 0
        # req==2: must have credit (pm & 2) > 0
        # req==3: must have at least one side used (pm != 0)
        if req == 1 and (pm & 1) == 0:
            return False  # Debit required but not used
        if req == 2 and (pm & 2) == 0:
            return False  # Credit required but not used
        if req == 3 and pm == 0:
            return False  # Both sides required but none used (this logic is stricter than the original)

    return True


def _accounts_score(pred_entries: List[dict], required_list: List[dict], side_zero_tol: float = 1e-6) -> float:
    """
    Soft scoring that rewards having at least one required side used.
    For req=3, gives full score if both sides used, 0.5 if one side used.
    """
    req_items = required_list or []
    if not req_items:
        return 0.0

    pred_map = _class_side_map_from_entries(pred_entries, side_zero_tol=side_zero_tol)

    total = 0.0
    n = 0
    for item in req_items:
        cls = str(item.get("account_class", "")).strip()
        req = int(item.get("side_mask", 0))
        if not cls or req == 0:
            continue

        pm = int(pred_map.get(cls, 0))
        req_bits = _bitcount(req)
        if req_bits == 0:
            continue

        if req == 3:
            # If both sides used, full credit (2/2)
            if pm == 3:
                overlap = 2
            # If one side used, half credit (1/2)
            elif pm != 0:
                overlap = 1
            else:
                overlap = 0
            total += overlap / req_bits
        else:
            overlap = _bitcount(pm & req)
            total += overlap / req_bits
            
        n += 1

    return (total / n) if n else 0.0





def _bitcount(x: int) -> int:
    """Count number of bits set in a 2-bit number"""
    return int(bin(int(x) & 0b11).count("1"))


def _accounts_score(pred_entries: List[dict], required_list: List[dict], side_zero_tol: float = 1e-6) -> float:
    """
    SOFT score in [0,1].
    score_i = overlap_bits / required_bits for each required class.
    """
    req_items = required_list or []
    if not req_items:
        return 0.0

    pred_map = _class_side_map_from_entries(pred_entries, side_zero_tol=side_zero_tol)

    total = 0.0
    n = 0
    for item in req_items:
        cls = str(item.get("account_class", "")).strip()
        req = int(item.get("side_mask", 0))
        if not cls or req == 0:
            continue

        pm = int(pred_map.get(cls, 0))
        req_bits = _bitcount(req)
        if req_bits == 0:
            continue

        overlap = _bitcount(pm & req)
        total += overlap / req_bits
        n += 1

    return (total / n) if n else 0.0


# ---------- lm-eval hooks ----------

def process_docs(dataset: datasets.Dataset) -> datasets.Dataset:
    """
    Adds req_account_sides computed from gold label.
    We force recompute to avoid cached old schema.
    """
    def _map(doc: dict) -> dict:
        convo = doc["conversations"]
        prompt = _unwrap_tuple_wrapped_text(convo[0]["content"])
        target = convo[1]["content"]

        gold_obj = _extract_first_json_object(target) or {}
        req_list = _required_list_from_gold(gold_obj)

        return {
            "prompt": prompt,
            "target": target,
            "req_account_sides": req_list,
        }

    return dataset.map(_map)


def process_results(doc: dict, results: List[str]) -> Dict[str, float]:
    text = results[0] if results else ""
    pred_entries = _extract_entries_from_text(text)

    parsed = 1.0 if len(pred_entries) > 0 else 0.0
    if not parsed:
        return {
            "parsed": 0.0,
            "balanced": 0.0,
            "accounts_correct_strict": 0.0,
            "accounts_correct_flexible": 0.0,
            "accounts_score_strict": 0.0,
            "accounts_score_flexible": 0.0,
            "balanced_and_score_strict": 0.0,
            "balanced_and_score_flexible": 0.0,
            "balanced_and_accounts_strict": 0.0,
            "balanced_and_accounts_flexible": 0.0,
            "correct_strict": 0.0,
            "correct_flexible": 0.0,
        }

    balanced = 1.0 if _balanced_from_entries(pred_entries, tol=1e-2) else 0.0

    req_list = doc.get("req_account_sides", []) or []

    accounts_correct = 1.0 if _accounts_correct(pred_entries, req_list) else 0.0
    accounts_score = float(_accounts_score(pred_entries, req_list))

    threshold = 0.5
    balanced_and_score = float(balanced) * accounts_score
    balanced_and_accounts = 1.0 if (balanced and accounts_score >= threshold) else 0.0

    return {
        "parsed": parsed,
        "balanced": balanced,
        "accounts_correct": accounts_correct,
        "accounts_score": accounts_score,
        "balanced_and_score": balanced_and_score,
        "balanced_and_accounts": balanced_and_accounts,
    }




 
