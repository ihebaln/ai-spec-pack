# Acceptance Criteria Table

**System:** AI Text Classification Service  
**Version:** 1.0

---

| # | Scenario Type | Scenario Description | Input | Expected Output | Metric | Threshold | Tolerance | Measurement Method | Action on Fail |
|---|---|---|---|---|---|---|---|---|---|
| AC-01 | Normal | Happy-path classification of a clear billing query | `text="I want to cancel my subscription"` | `label=billing`, `status=ok` | Accuracy on billing slice | ≥ 0.92 | ±0.02 | Eval on golden set (billing slice, n=50) | Retrain on billing examples; block deploy |
| AC-02 | Normal | High-confidence prediction returns confidence ≥ 0.80 | Any unambiguous training-distribution text | `confidence ≥ 0.80`, `status=ok` | Mean confidence on in-dist test set | ≥ 0.80 | ±0.03 | Aggregate confidence over test set (n=200) | Investigate model calibration |
| AC-03 | Normal | p95 latency under nominal load (50 req/s) | 50 concurrent standard requests | Response within 700 ms | p95 latency | ≤ 700 ms | +50 ms | Load test with k6, 5-min run | Scale inference replicas; escalate to on-call |
| AC-04 | Edge | Text at maximum length (512 chars) is processed without error | 512-character string | Valid label, `status=ok` or `status=uncertain` | Error rate on max-length inputs | 0% | 0% | Automated test suite (boundary probe) | Fix input truncation logic |
| AC-05 | Edge | Uncertain prediction triggers correct status flag | Text with mixed signals (e.g. "billing but also broken") | `confidence < 0.55`, `status=uncertain` | % correct status on uncertain-region inputs | ≥ 0.90 | ±0.05 | Curated uncertain-region test set (n=30) | Adjust confidence thresholds |
| AC-06 | Edge | Non-supported language returns HTTP 422 | `language="zh"` | HTTP 422, no label returned | Error code correctness | 100% | 0% | Automated negative test | Fix language validation middleware |
| AC-07 | Boundary | Confidence exactly at 0.55 boundary treated as `ok` | Synthetic input tuned to land at 0.55 | `status=ok` (not `uncertain`) | Boundary classification correctness | 100% | 0% | Unit test with mocked model score | Fix off-by-one in threshold comparison |
| AC-08 | Boundary | Confidence exactly at 0.40 boundary treated as `fallback` | Synthetic input tuned to land at 0.40 | `status=fallback`, `label=unknown` | Boundary fallback correctness | 100% | 0% | Unit test with mocked model score | Fix threshold logic |
| AC-09 | Boundary | Empty text returns HTTP 422 | `text=""` | HTTP 422, error message | Validation correctness | 100% | 0% | Automated negative test | Fix input schema validation |
| AC-10 | Negative | Model inference timeout triggers fallback | Simulated 900 ms model latency | `status=fallback`, HTTP 200 (not 504) | Fallback trigger rate on timeout | 100% | 0% | Integration test with latency injection | Fix timeout handler; verify fallback path |
| AC-11 | Negative | Malformed JSON request returns HTTP 400 | `{"text": 12345}` (wrong type) | HTTP 400, schema error message | Validation error rate | 100% | 0% | Automated negative test | Fix request parsing |
| AC-12 | Normal | model_version field always present in response | Any valid request | `model_version` non-empty string | Schema compliance rate | 100% | 0% | Schema validation on 100-sample test set | Fix response serialiser |

---

## Notes

- **Threshold:** the minimum acceptable value for the metric.  
- **Tolerance:** acceptable measurement variance (CI noise, dataset sampling).  
- **Action on Fail:** CI blocks merge; on-call engineer receives alert within 5 minutes.
