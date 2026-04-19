# Dataset Card — Intent Classification Dataset v1.0

---

## Dataset Summary

A multi-source dataset of short customer service messages labelled with intent categories for use in training and evaluating a text classification model.

---

## Source

| Source | Description |
|---|---|
| `internal_tickets` | Anonymised support tickets from a SaaS product (2021–2023), PII removed |
| `synthetic_gpt4` | GPT-4 generated examples, reviewed by 2 annotators |
| `crowdsource_v1` | Amazon Mechanical Turk, 2023-Q4 campaign |

---

## Purpose

Train, validate, and evaluate an intent classification model for automated routing of customer messages.

---

## Intended Use

- Training supervised classification models.
- Offline evaluation and regression testing.
- Threshold calibration.

## Non-Intended Use (Do Not Use For)

- Real-time PII detection or handling.
- Any purpose requiring personal identification of individuals.
- Tasks outside customer-service intent classification.
- Training generative models.

---

## Composition

| Split | Records | % |
|---|---|---|
| Train | ~700 | 70% |
| Validation | ~150 | 15% |
| Test | ~150 | 15% |
| **Total** | **~1 000** | 100% |

**Label distribution (approximate):**

| Label | % |
|---|---|
| billing | 20% |
| technical_support | 18% |
| account_management | 17% |
| sales_inquiry | 15% |
| complaint | 12% |
| compliment | 10% |
| other | 8% |

---

## Labelling

- Internal tickets: labelled by 2 trained annotators with adjudication on disagreement. Inter-annotator agreement (Cohen's κ) = 0.84.
- Synthetic: labelled by the generation prompt; verified by 1 reviewer.
- Crowdsource: majority vote of 3 annotators; records with 2/3 disagreement discarded.

---

## Known Limitations

- English-only (v1.0).
- Synthetic examples may not reflect natural phrasing variation.
- `other` class is sparse and may underperform.
- Source distribution may not match all deployment domains.

---

## Versions

| Version | Date | Notes |
|---|---|---|
| 1.0 | 2024-04-19 | Initial release |

---

## Contact

ML Platform Team — see repo CODEOWNERS.
