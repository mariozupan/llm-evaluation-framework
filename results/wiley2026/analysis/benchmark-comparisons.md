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



#### GPT-OSS-20B

```text
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
```



#### GLM-4-5-Air

```text
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
```




### Demostration of the evaluation of individual samples

In the following simple example the LLM predicts correctly the posting scheme for one of the many various types of input invoices. As it can be seen the LLM provide a transparent input invoice scheme. However lm eval harness evaluation was done in one-shot prompting where the evaluated code rated accounts correctness with 0.75 because the latest account prediction differs from the target, no matter what the balance and the side was correct.

However the threshold for Accounts Correct (balanced AND business logical)' was set to the 0.5:

```
#################################################
    threshold = 0.5
#################################################
evaluation['balanced_and_accounts'] = 1.0 if (evaluation['balanced'] == 1.0 and evaluation['accounts_score'] >= threshold) else 0.0

```

It is always hard to make decision on heuristic outputs but the decision for different fine-tuning configurations was transparent because the structure of posting schemes on which models have been trained is relying on the accounting information system which was made on mostly generative scheme, connected with the unique codenames where usually 50% of autocompleted i.e. suggested journal accounts are usually changed by the user. 

So this example will be evaluated as 'Accounts correct' 
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

