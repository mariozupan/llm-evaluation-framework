# Wiley 2026 Evaluation Results

This directory contains complete evaluation results for the bookkeeping LLM fine-tuning study described in the research paper "An evaluation framework for post-trained bookkeeping language models".

## Directory Structure

```
wiley2026/
├── base-models/           # Pre-trained model evaluation results
│   ├── seed-oss-36b-base/     # Seed-OSS-36B base model performance
│   ├── gpt-oss-20b-base/      # GPT-OSS-20B base model performance  
│   └── glm-4-5-air-base/      # GLM-4-5-Air base model performance
├── fine-tuned-models/     # Fine-tuned model evaluation results
│   ├── seed-oss-36b-qlora/    # Seed-OSS-36B with QLoRA fine-tuning
│   ├── gpt-oss-20b-fft/       # GPT-OSS-20B with full fine-tuning
│   └── glm-4-5-air-qlora/     # GLM-4-5-Air with QLoRA fine-tuning
└── analysis/              # Statistical analysis and comparisons
    └── benchmark-comparisons.md
```

## Methodology

### Evaluation Framework

- **Language Model Evaluation Harness (lm-eval)**: Used for reproducible benchmarking
- **Custom bookkeeping task**: Six-domain evaluation (parsed, balanced, accounts_correct, accounts_score, balanced&score, balanced&accounts)
- **Standard benchmarks**: HellaSwag, MMLU, TruthfulQA, WinoGrande, ARC-Easy, GSM8K, IFEval

### Hardware Configuration

- **HPC Cluster**: 4× NVIDIA PG506-232 GPUs (96GB VRAM each)
- **Total Memory**: 384GB GPU memory
- **Training Framework**: Axolotl with FSDP2, mixed precision (bfloat16)

### Fine-tuning Methods

- **QLoRA**: 4-bit quantization with low-rank adapters (target: linear layers)
- **FFT**: Full parameter fine-tuning with DeepSpeed ZeRO Stage 3
- **Memory Constraints**: Dictated method selection based on model size


