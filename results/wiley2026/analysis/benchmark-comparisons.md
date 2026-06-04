# Benchmark Comparisons Analysis

> *My reaction is that there is an evaluation crisis. I don't really know what metrics to look at right now.*
> *MMLU was a good and useful for a few years but that's long over.*
> *SWE-Bench Verified (real, practical, verified problems) I really like and is great but itself too narrow.*
> *Chatbot Arena received so much focus (partly my fault?) that LLM labs have started to really overfit to it, via a combination of prompt mining (from API requests), private evals bombardment, and, worse, explicit use of rankings as training supervision. I think it's still ~ok and there's a lack of "better", but it feels on decline in signal.*
> *There's a number of private evals popping up, an ensemble of which might be one promising path forward.*
> *In absence of great comprehensive evals I tried to turn to vibe checks instead, but I now fear they are misleading and there is too much opportunity for confirmation bias, too low sample size, etc., it's just not great.*
>
> *TLDR my reaction is I don't really know how good these models are right now.*

— Andrey Karpathy, [X/Twitter post](https://x.com/karpathy/status/1896266683301659068), 2025



## Model Comparison Summary

### General benchmark performance

| Model | Method | MMLU | GSM8K | HellaSwag |
|-------|--------|------|-------|-----------|
| **Seed-OSS-36B** | Base | 0.230 | 0.115 | 0.683 |
| **Seed-OSS-36B** | QLoRA | **0.514** | 0.289 | **0.740** |
| **GPT-OSS-20B** | Base | 0.272 | 0.650 | 0.330 |
| **GPT-OSS-20B** | FFT | 0.229 | **0.453** | 0.453 |
| **GLM-4-5-Air** | Base | 0.583 | 0.261 | 0.676 |
| **GLM-4-5-Air** | QLoRA | 0.331 | 0.396 | 0.708 |



### Bookkeeping Performance

#### Seed-OSS-36B 

```text
⚙️  Evaluating samples for model: seed-oss
   Processing samples from .eval-workspace/samples/seed-oss/samples.jsonl
   Processed 1615 samples
   ✅ Saved evaluations to .eval-workspace/evaluations/seed-oss/evaluations.jsonl

📊 EVALUATION SUMMARY:
   Total samples: 1615
   ✅ Accounts Correct (balanced AND business logical): 1425 (88.2%)
   ⚖️  Balanced: 1599 (99.0%)
   📊 Accounts Score: 73.11%
   ❌ Incorrect: 190 (11.8%)
``` 



#### GPT-OSS-20B

```text
⚙️  Evaluating samples for model: gpt-oss
   Processing samples from .eval-workspace/samples/gpt-oss/samples.jsonl
   Processed 1615 samples
   ✅ Saved evaluations to .eval-workspace/evaluations/gpt-oss/evaluations.jsonl

📊 EVALUATION SUMMARY:
   Total samples: 1615
   ✅ Accounts Correct (balanced AND business logical): 967 (59.9%)
   ⚖️  Balanced: 1156 (71.6%)
   📊 Accounts Score: 55.45%
   ❌ Incorrect: 648 (40.1%)
```



#### GLM-4-5-Air

```text
⚙️  Evaluating samples for model: glm
   Processing samples from .eval-workspace/samples/glm/samples.jsonl
   Processed 1615 samples
   ✅ Saved evaluations to .eval-workspace/evaluations/glm/evaluations.jsonl

📊 EVALUATION SUMMARY:
   Total samples: 1615
   ✅ Accounts Correct (balanced AND business logical): 801 (49.6%)
   ⚖️  Balanced: 1343 (83.2%)
   📊 Accounts Score: 40.57%
   ❌ Incorrect: 814 (50.4%)
```
```
```




### Demonstration of the evaluation of individual samples

In the following simple example, the LLM correctly predicts the posting scheme for one of the many different types of input invoices. As can be seen, the LLM provides a transparent input invoice scheme. However, the LM Evaluation Harness evaluation was done using one-shot prompting, where the evaluation code rated account correctness as 0.75 because the last account prediction differs from the target, even though the balance and the side were correct.

However, the threshold for Accounts Correct (balanced AND business logical) was set to 0.5.


```
#################################################
    threshold = 0.5
#################################################
evaluation['balanced_and_accounts'] = 1.0 if (evaluation['balanced'] == 1.0 and evaluation['accounts_score'] >= threshold) else 0.0

```
It is always hard to make decisions based on stohastic outputs, but the decision for different fine-tuning configurations was transparent because the structure of the posting schemes on which the models were trained relies on an accounting information system. This system was built mostly on a generative scheme connected with unique codenames, where usually 50% of autocompleted, i.e. suggested, journal accounts are changed by the user.

So this example, according to the selected threshold, will be evaluated as **Accounts Correct** in the model evaluation summaries above.

```text

================================================================================
📋 SAMPLE 2 EVALUATION DETAILS
================================================================================

📝 TARGET:
{
  "year": "2019",
  "document": "URAEU",
  "document_explanation": "Document codename for posting various types of input invoices. These can include invoices for different costs, such as electricity, fuel, goods received into stock according to the delivery note, small inventory, and services like telecommunications, banking, and forwarding.",
  "total_debit": 15350.7,
  "total_credit": 15350.7,
  "entries": [
    {
      "ACCOUNT": "140000",
      "TITLE": "PRE**********************************",
      "DEBIT": 3070.14,
      "CREDIT": 0.0
    },
    {
      "ACCOUNT": "220",
      "TITLE": "TER*****************",
      "DEBIT": 0.0,
      "CREDIT": 15350.7
    },
    {
      "ACCOUNT": "224",
      "TITLE": "TER*****************",
      "DEBIT": 12280.56,
      "CREDIT": 0.0
    }
  ]
}

🤖 PREDICTION:
{
  "year": "2019",
  "document": "URAEU",
  "total_debit": 1000.0,
  "total_credit": 1000.0,
  "entries": [
    {
      "ACCOUNT": "140000",
      "TITLE": "PRE**********************************",
      "DEBIT": 200.0,
      "CREDIT": 0.0
    },
    {
      "ACCOUNT": "220",
      "TITLE": "AUT***************************************",
      "DEBIT": 0.0,
      "CREDIT": 1000.0
    },
    {
      "ACCOUNT": "4111",
      "TITLE": "USL*********************************",
      "DEBIT": 800.0,
      "CREDIT": 0.0
    }
  ]
}

📊 EVALUATION METRICS:
  Parsed: 1.0
  Balanced: 1.0
  Accounts Score: 0.7500

🎯 REQUIRED ACCOUNT SIDES:
  Account class 14: debit only (mask=1)
  Account class 22: both sides (mask=3)

```
```
```

