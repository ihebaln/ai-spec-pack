# DataContract — Text Classification Dataset

**Version:** 1.0  
**Date:** 2024-04-19  
**Owner:** ML Platform Team

---

## 1. Purpose

This contract defines the invariants that the dataset MUST satisfy at every pipeline stage (ingest, train, eval). CI will fail if any check listed in §3 is violated.

---

## 2. Invariants

| ID | Invariant | Severity |
|---|---|---|
| DC-01 | File is valid CSV (parseable, correct delimiter) | CRITICAL |
| DC-02 | All required columns present: `id, text, label, language, source, split` | CRITICAL |
| DC-03 | No record has an empty `text` field | CRITICAL |
| DC-04 | All `label` values are in the allowed set | CRITICAL |
| DC-05 | No duplicate `id` values | HIGH |
| DC-06 | No `text` field duplicated across train and test splits | HIGH |
| DC-07 | `split` column only contains `train`, `val`, `test` | HIGH |
| DC-08 | No single class exceeds 50% of total records | MEDIUM |
| DC-09 | No single source dominates > 70% of records | MEDIUM |
| DC-10 | Text length distribution: p99 ≤ 512 characters | HIGH |

---

## 3. Automated Checks

All checks are implemented in `tests/test_data_checks.py` and run via `make data-check`.

---

## 4. Versioning

- Dataset versions follow `MAJOR.MINOR` (e.g. `1.0`, `1.1`).
- Any change to the label set is a MAJOR version bump.
- Changes to source proportions or splits are MINOR bumps.
- Version is recorded in the filename: `data/dataset_v1.0.csv`.

---

## 5. Refresh Cadence

- Full refresh: quarterly.
- Incremental additions: monthly, subject to same contract checks.
- After each refresh, all CI checks must pass before the new version is promoted to `latest`.
