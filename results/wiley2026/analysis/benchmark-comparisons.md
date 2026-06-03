# Benchmark Comparisons Analysis


## Model Comparison Summary

### Based knowledge Performance

| Model | Method | MMLU | GSM8K | HellaSwag |
|-------|--------|------|-------|-----------|
| **Seed-OSS-36B** | Base | 0.230 | 0.115 | 0.683 |
| **Seed-OSS-36B** | QLoRA | **0.514** | 0.289 | **0.740** |
| **GPT-OSS-20B** | Base | 0.272 | 0.650 | 0.330 |
| **GPT-OSS-20B** | FFT | 0.229 | 0.453 | 0.453 |
| **GLM-4-5-Air** | Base | 0.583 | 0.261 | 0.676 |
| **GLM-4-5-Air** | QLoRA | 0.331 | **0.396** | 0.708 |



### Bookkeeping Performance

#### Seed-OSS-36B 

```text
```text
⚙️  Evaluating samples for model: seed-oss
   Processing samples from .eval-workspace/samples/seed-oss/samples.jsonl
   Processed 1615 samples
   ✅ Saved evaluations to .eval-workspace/evaluations/seed-oss/evaluations.jsonl

📊 EVALUATION SUMMARY:
   Total samples: 1615
   ✅ Accounts Correct (balanced AND business logical): 682 (42.2%)
   ⚖️  Balanced: 1599 (99.0%)
   📊 Accounts Score: 73.11%
   ❌ Incorrect: 933 (57.8%)
``` 



```
#### GPT-OSS-20B

```text
```
⚙️  Evaluating samples for model: gpt-oss
   Processing samples from .eval-workspace/samples/gpt-oss/samples.jsonl
   Processed 1615 samples
   ✅ Saved evaluations to .eval-workspace/evaluations/gpt-oss/evaluations.jsonl

📊 EVALUATION SUMMARY:
   Total samples: 1615
   ✅ Accounts Correct (balanced AND business logical): 694 (43.0%)
   ⚖️  Balanced: 1156 (71.6%)
   📊 Accounts Score: 55.45%
   ❌ Incorrect: 921 (57.0%)
```text
```



#### GLM-4-5-Air
```text
```

⚙️  Evaluating samples for model: glm
   Processing samples from .eval-workspace/samples/glm/samples.jsonl
   Processed 1615 samples
   ✅ Saved evaluations to .eval-workspace/evaluations/glm/evaluations.jsonl

📊 EVALUATION SUMMARY:
   Total samples: 1615
   ✅ Accounts Correct (balanced AND business logical): 100 (6.2%)
   ⚖️  Balanced: 1343 (83.2%)
   📊 Accounts Score: 40.57%
   ❌ Incorrect: 1515 (93.8%)
```
```



#### The evaluation on individual sample



