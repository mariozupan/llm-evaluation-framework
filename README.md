# LLM Evaluation Framework for Bookkeeping Posting Schemes

This repository contains the evaluation framework and training configurations used for fine-tuning and evaluating large language models on double-entry bookkeeping posting schemes, as described in the accompanying research paper.

## Repository Structure

```
llm-evaluation-framework/
├── src-axolotl/                    # Training configurations
│   ├── wiley-2026-gpt-oss-20b-fft-fsdp2-IMPROVED.yaml
│   ├── wiley-2026-seed-oss-36b-qlora-default-config.yaml
│   └── wiley-2026-GLM-4-5-Air.yaml
│
└── src-lm-eval-harness/          # Evaluation task definitions
    └── tasks-bookkeeping/
        └── bookkeeping_posting_schemes/
            ├── bookkeeping_posting_schemes.yaml   # Task configuration
            └── utils.py                 # Scoring utilities
```

## Training Configurations (`src-axolotl/`)

Three Axolotl YAML configuration files for fine-tuning:

| Model | Method | GPU Memory |
|-------|-------|-----------|
| GPT-OSS-20B | Full Fine-Tuning (FFT) | ~80 GB |
| Seed-OSS-36B | QLoRA (4-bit) | ~35 GB |
| GLM-4-5-Air | QLoRA (4-bit) | ~64 GB |

### Usage

```bash
# Install axolotl
pip install axolotl

# Fine-tune a model
axolotl train src-axolotl/wiley-2026-seed-oss-36b-qlora-default-config.yaml
```

## Evaluation Task (`src-lm-eval-harness/`)

The bookkeeping evaluation task implements six metrics:

1. **parsed** - Model output contains valid JSON
2. **balanced** - Total debits equals total credits
3. **accounts_correct** - All account codes are valid
4. **accounts_score** - Correct account codes used
5. **balanced&score** - Both balanced and correct accounts
6. **balanced&accounts** - Balanced and account score ≥ threshold

### Usage

```bash
# Install lm-eval
pip install lm-eval

# Evaluate a model
lm-eval \
  --model huggingface \
  --model_args pretrained=path/to/model \
  --tasks bookkeeping_posting_schemes \
  --output_path results.json
```

### Task Configuration

The evaluation task:
- Uses greedy decoding (temperature=0)
- Generates up to 512 tokens
- Parses JSON from model output
- Validates debit/credit balancing and account codes

## Key Results

| Model | Method | Accounts Score | Balanced |
|-------|--------|--------------|----------|
| Seed-OSS-36B | QLoRA | 0.731 | 0.990 |
| GPT-OSS-20B | FFT | 0.736 | 0.955 |
| GLM-4-5-Air | QLoRA | 0.406 | 0.832 |

See the paper for full evaluation methodology and results.

## Requirements

- Python 3.10+
- CUDA-capable GPU (4×96GB recommended)
- Axolotl
- lm-eval-harness
- Transformers + PEFT

## License

Apache 2.0

## Citation

If you use this code in your research, please cite:

```
@article{zupan2026bookkeeping,
  title={Fine-tuning and Evaluating LLMs on Double-Entry Bookkeeping Posting Schemes},
  author={Zupan, Mario},
  year={2026}
}
```