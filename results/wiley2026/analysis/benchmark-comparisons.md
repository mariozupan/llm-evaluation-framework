# Benchmark Comparisons Analysis

## Overview

This document provides detailed comparative analysis across different models and fine-tuning methods, highlighting key insights from the evaluation results. The analysis addresses the core research question: how do different fine-tuning methods affect domain knowledge acquisition and general capability preservation?

## Model Comparison Summary

### Performance by Model and Method

| Model | Method | MMLU | GSM8K | HellaSwag | Accounts Correct | Balanced |
|-------|--------|------|-------|-----------|-----------------|----------|
| **Seed-OSS-36B** | Base | 0.230 | 0.115 | 0.683 | N/A | N/A |
| **Seed-OSS-36B** | QLoRA | **0.514** | 0.289 | **0.740** | 0.424 | 0.990 |
| **GPT-OSS-20B** | Base | 0.272 | 0.650 | 0.330 | N/A | N/A |
| **GPT-OSS-20B** | FFT | 0.229 | 0.453 | 0.453 | **0.518** | 0.955 |
| **GLM-4-5-Air** | Base | 0.583 | 0.261 | 0.676 | N/A | N/A |
| **GLM-4-5-Air** | QLoRA | 0.331 | **0.396** | 0.708 | 0.087 | 0.832 |



