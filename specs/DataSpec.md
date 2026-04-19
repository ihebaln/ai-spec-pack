# DataSpec — Text Classification Dataset

**Version:** 1.0  
**Date:** 2024-04-19

---

## 1. Overview

Training and evaluation data for the intent classification model.  
Each record is a short customer-facing text message labelled with one of 7 intent classes.

---

## 2. Schema

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string (UUID) | Yes | Unique record identifier |
| `text` | string | Yes | Raw input text, 1–512 chars |
| `label` | string | Yes | Ground-truth intent class |
| `language` | string | Yes | ISO 639-1 code |
| `source` | string | Yes | Origin of the record (see §4) |
| `split` | string | Yes | `train`, `val`, or `test` |
| `annotator_id` | string | No | Anonymised annotator identifier |
| `annotation_date` | date | No | ISO 8601 date of labelling |

---

## 3. Label Set

`billing` | `technical_support` | `account_management` | `sales_inquiry` | `complaint` | `compliment` | `other`

---

## 4. Sources

| Source ID | Description | Proportion |
|---|---|---|
| `internal_tickets` | Anonymised historical support tickets | 60% |
| `synthetic_gpt4` | GPT-4 generated examples for minority classes | 25% |
| `crowdsource_v1` | Annotated via Mechanical Turk campaign 2023-Q4 | 15% |

---

## 5. Split Ratios

| Split | Proportion |
|---|---|
| Train | 70% |
| Validation | 15% |
| Test | 15% |

Test set is held out and never used during training or hyperparameter search.

---

## 6. Preprocessing

1. Strip leading/trailing whitespace.
2. Truncate to 512 characters.
3. Remove records where `text` is empty after stripping.
4. Normalise Unicode to NFC.
5. No lowercasing (model handles casing natively).

---

## 7. Known Limitations

- `other` class is intentionally underrepresented (≈8%) to match real-world distribution.
- Synthetic examples may have higher lexical uniformity than real data.
- Language coverage: English only in v1.0; multilingual extension planned for v2.0.
