# ModelSpec — Intent Classification Model

**Version:** 1.0  
**Date:** 2024-04-19

---

## 1. Baseline

| Property | Value |
|---|---|
| Model type | Fine-tuned transformer (DistilBERT-base-uncased) |
| Baseline comparator | TF-IDF + Logistic Regression |
| Baseline macro-F1 | 0.74 |
| Target macro-F1 | ≥ 0.85 |
| Training framework | HuggingFace Transformers + PyTorch |
| Training dataset | `data/dataset_v1.0.csv` (train split) |

The model must beat the baseline on every tracked slice before deployment.

---

## 2. Applicability Limits

The model is **only applicable** when:

- Input language is `en` (English).
- Input text is 1–512 characters.
- Domain is customer service intent (the 7 defined classes).

The model is **NOT applicable** for:

- Multilingual input (v1.0).
- Long documents (> 512 chars).
- Sentiment analysis, NER, or generative tasks.
- Highly technical/domain-specific jargon outside support context.

If an input is outside these limits, the service must reject it (HTTP 422) or route to fallback.

---

## 3. Resource Envelope

| Resource | Budget |
|---|---|
| Inference latency (p95) | ≤ 700 ms |
| Inference latency (p99) | ≤ 1 000 ms |
| GPU memory per replica | ≤ 2 GB |
| CPU fallback memory | ≤ 1 GB |
| Cost per request | ≤ $0.002 |
| Max model size on disk | ≤ 300 MB |
| Replicas (steady-state) | 2 minimum |

---

## 4. Update Policy

| Trigger | Action |
|---|---|
| Macro-F1 drops > 3% vs previous version | Automatic rollback; retrain investigation |
| New label class required | MAJOR version bump; full retrain |
| Data refresh (quarterly) | Incremental fine-tune; full eval gate must pass |
| Production accuracy degrades (monitoring alert) | Emergency retrain within 5 business days |
| Model > 6 months old | Scheduled review and retrain |

**Deployment process:**  
1. Eval gate must pass (see `EvalPlan.md`).  
2. Shadow deployment for 24 h.  
3. Canary at 10% traffic for 48 h.  
4. Full rollout with automatic rollback on error-rate spike.

---

## 5. Versioning

Models follow `MAJOR.MINOR.PATCH` (e.g., `1.0.0`).  
Model version is embedded in every API response via `model_version` field.
