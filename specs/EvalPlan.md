# EvalPlan — Intent Classification Model

**Version:** 1.0  
**Date:** 2024-04-19

---

## 1. Metrics

| Metric | Description | Gate Threshold |
|---|---|---|
| `macro_f1` | Unweighted mean F1 across all 7 classes | ≥ 0.85 |
| `accuracy` | Overall accuracy on test set | ≥ 0.87 |
| `billing_f1` | Per-class F1 for `billing` | ≥ 0.88 |
| `technical_support_f1` | Per-class F1 for `technical_support` | ≥ 0.86 |
| `complaint_f1` | Per-class F1 for `complaint` | ≥ 0.82 |
| `other_f1` | Per-class F1 for `other` (sparse class) | ≥ 0.65 |
| `latency_p95_ms` | 95th percentile inference latency | ≤ 700 |
| `fallback_rate` | Fraction of requests returning `status=fallback` | ≤ 0.05 |

---

## 2. Evaluation Slices

Eval must be run and reported separately on each slice. A model that passes overall but fails any slice is **blocked**.

| Slice ID | Description |
|---|---|
| `slice_billing` | Records with label = `billing` |
| `slice_technical_support` | Records with label = `technical_support` |
| `slice_complaint` | Records with label = `complaint` |
| `slice_other` | Records with label = `other` (minority class) |
| `slice_synthetic` | Records where source = `synthetic_gpt4` |
| `slice_crowdsource` | Records where source = `crowdsource_v1` |
| `slice_short_text` | Records where `len(text) < 50` |
| `slice_long_text` | Records where `len(text) > 300` |

---

## 3. Thresholds & Gates

Gates are defined in `configs/thresholds.yaml` and enforced by `src/eval_gate.py`.

**CI fails if any of the following are violated:**

1. `macro_f1 < 0.85`
2. `accuracy < 0.87`
3. `billing_f1 < 0.88`
4. `technical_support_f1 < 0.86`
5. `complaint_f1 < 0.82`
6. `other_f1 < 0.65`
7. `latency_p95_ms > 700`
8. `fallback_rate > 0.05`

---

## 4. Regression Rule

A new model version is **blocked from deployment** if:

- `macro_f1` decreases by more than **0.03 absolute** compared to the previous passing version (recorded in `reports/metrics.json`).
- Any per-class F1 in slices 1–4 decreases by more than **0.05 absolute** compared to the previous version.

Regression is checked automatically by the eval gate script.

---

## 5. Golden Set

File: `data/golden_set.jsonl`  
Size: 30 curated examples (see file).  
Purpose: Smoke test that runs on every CI push. If the model (or mock model) does not score ≥ 0.90 accuracy on the golden set, CI fails.

The golden set is **frozen** — it may only be extended (never modified) via a PR with two reviewers.

---

## 6. Measurement Procedure

1. Load the test split from `data/dataset_v1.0.csv`.
2. Run inference on all test records.
3. Compute all metrics and write to `reports/metrics.json`.
4. Run `src/eval_gate.py` to compare against `configs/thresholds.yaml`.
5. Gate script exits with code 0 (pass) or 1 (fail).
