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
├── src-lm-eval-harness/          # Evaluation task definitions
│   └── tasks-bookkeeping/
│       └── bookkeeping_posting_schemes/
│           ├── bookkeeping_posting_schemes.yaml   # Task configuration
│           └── utils.py                 # Scoring utilities
│
└── results/                       # Complete evaluation results
    └── wiley2026/
        ├── base-models/           # Pre-trained model results
        ├── fine-tuned-models/     # Fine-tuned model results
        ├── analysis/              # Statistical analysis
        └── README.md              # Results documentation
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

### Bookkeeping Domain Performance

| Model | Method | Accounts Score | Balanced |
|-------|--------|--------------|----------|
| Seed-OSS-36B | QLoRA | 0.731 | 0.990 |
| GPT-OSS-20B | FFT | 0.736 | 0.955 |
| GLM-4-5-Air | QLoRA | 0.406 | 0.832 |

### General Knowledge Preservation

| Benchmark | Base | Seed-OSS QLoRA | GPT-OSS FFT | GLM-4-5-Air QLoRA |
|-----------|------|---------------|-----------|------------------|
| HellaSwag | 0.683 | **0.740** | 0.453 | 0.708 |
| MMLU | 0.230 | **0.514** | 0.229 | 0.331 |
| TruthfulQA | 0.356 | 0.357 | **0.370** | 0.354 |
| GSM8K | 0.115 | 0.289 | 0.455 | **0.396** |

## Complete Results & Reproducibility

### Full Evaluation Results

The complete evaluation results are available in the `results/wiley2026/` directory:

- **Base Models**: Pre-trained model performance on all benchmarks
- **Fine-tuned Models**: Performance after domain fine-tuning
- **Statistical Analysis**: Detailed significance testing and effect sizes
- **Benchmark Comparisons**: Cross-model and cross-method analysis

### Accessing Complete Results

```bash
# Navigate to results directory
cd results/wiley2026/

# View available results
ls -la
# ├── base-models/
# ├── fine-tuned-models/
# ├── analysis/
# └── README.md
```

### Reproducing Results

1. **Install Dependencies**:
   ```bash
   pip install lm-eval axolotl transformers peft
   ```

2. **Evaluate Base Models**:
   ```bash
   # Seed-OSS-36B base model
   lm-eval --model huggingface \
     --model_args pretrained=ByteDance-Seed/Seed-OSS-36B-Instruct \
     --tasks mmlu,gsm8k,hellaswag,truthfulqa,arc_easy,ifeval \
     --output_path results/base-models/seed-oss-36b/base_results.json
   ```

3. **Evaluate Fine-tuned Models**:
   ```bash
   # Seed-OSS-36B QLoRA fine-tuned
   lm-eval --model huggingface \
     --model_args pretrained=/path/to/seed-oss-36b-qlora \
     --tasks mmlu,gsm8k,hellaswag,truthfulqa,arc_easy,ifeval,bookkeeping_posting_schemes \
     --output_path results/fine-tuned-models/seed-oss-36b-qlora/results.json
   ```

4. **Custom Bookkeeping Evaluation**:
   ```bash
   lm-eval --model huggingface \
     --model_args pretrained=/path/to/model \
     --tasks bookkeeping_posting_schemes \
     --output_path bookkeeping_evaluation.json
   ```

### Statistical Validation

All reported improvements are statistically significant:
- **95% Confidence Intervals**: Non-overlapping intervals for major improvements
- **p-values**: < 0.001 for all major improvements
- **Effect Sizes**: Large effect sizes (d > 1.0) for significant improvements

See `results/wiley2026/analysis/statistical-significance.md` for detailed statistical analysis.

## Key Findings

1. **QLoRA preserves general knowledge**: Seed-OSS-36B QLoRA showed +123% improvement on MMLU (0.230→0.514) - counter-intuitive result showing structured accounting data provides beneficial training signal.

2. **FFT causes catastrophic forgetting**: GPT-OSS-20B FFT showed severe degradation on HellaSwag (-34%), WinoGrande (-25%), IFEval (-46%), despite strong domain performance.

3. **Gradient stability**: FFT has much higher gradient variance (mean 1.159, max 25.6) vs QLoRA (<0.15), affecting training stability.

4. **Memory efficiency**: QLoRA uses 49% less memory (35.2 GiB vs 80.1 GiB), enabling 36B models on 4×96GB GPUs.

5. **MoE challenges**: GLM-4-5-Air maintained general knowledge but struggled with structured generation, suggesting expert routing hinders low-rank adapter propagation.

## Requirements

- Python 3.10+
- CUDA-capable GPU (4×96GB recommended)
- Axolotl
- lm-eval-harness
- Transformers + PEFT

## License

MIT

## Citation

If you use this code in your research, please cite:

```
@article{zupan2026bookkeeping,
  title={Fine-tuning and Evaluating LLMs on Double-Entry Bookkeeping Posting Schemes},
  author={Zupan, Mario},
  year={2026}
}
```