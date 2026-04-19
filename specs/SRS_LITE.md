# SRS_LITE — AI Spec Pack: Text Classification Service

**Version:** 1.0  
**Date:** 2024-04-19  
**Status:** Draft

---

## 1. Purpose

This document specifies requirements for an AI-powered text classification service that categorises short text inputs (e.g. support tickets, customer messages) into a predefined set of intent categories.

---

## 2. Input / Output Schemas

### 2.1 Input Schema

```json
{
  "request_id": "string (UUID v4, required)",
  "text": "string (1–512 characters, required)",
  "language": "string (ISO 639-1, optional, default: 'en')",
  "context": "object (optional, arbitrary key-value metadata)"
}
```

**Constraints:**
- `text` must be non-empty and ≤ 512 characters (after stripping whitespace).
- `language` must be one of the supported codes: `en`, `sv`, `de`, `fr`.
- `request_id` must be a valid UUID v4.

### 2.2 Output Schema

```json
{
  "request_id": "string (UUID v4, echoed)",
  "label": "string (top predicted class)",
  "confidence": "float [0.0 – 1.0]",
  "alternatives": [
    { "label": "string", "confidence": "float" }
  ],
  "latency_ms": "integer",
  "model_version": "string",
  "status": "string (ok | uncertain | fallback | error)"
}
```

---

## 3. Degradation Rules

### 3.1 Timeouts

| Scenario | Threshold | Action |
|---|---|---|
| Model inference | > 800 ms | Return `status: fallback`, serve cached or rule-based response |
| Full request (incl. network) | > 1 200 ms | Return `status: error` with HTTP 504 |

### 3.2 Uncertainty Zone

- If `confidence < 0.55`: set `status: uncertain`, still return top label.
- If `confidence < 0.40`: set `status: fallback`, return label `"unknown"`, log for human review.

### 3.3 Fallback Behaviour

1. **Cached fallback:** return the most common label for the detected language from a static lookup table.
2. **Rule-based fallback:** apply keyword matching as a secondary signal.
3. **Hard failure:** if both fail, return HTTP 503 with `status: error`.

---

## 4. Non-Functional Requirements (NFRs)

### 4.1 Latency

| Percentile | Target |
|---|---|
| p50 | ≤ 300 ms |
| p95 | ≤ 700 ms |
| p99 | ≤ 1 000 ms |

Measured end-to-end at the API gateway under a steady-state load of 50 req/s.

### 4.2 Availability

- Target: **99.5% uptime** per calendar month.
- Planned maintenance windows excluded (max 2 h/month, announced 48 h in advance).

### 4.3 Cost

- Inference cost target: **≤ $0.002 per request** at p95 load.
- Monthly compute budget cap: **$500**.
- Cost monitored weekly; alert if 7-day rolling average exceeds 110% of target.

---

## 5. Supported Classes

`billing`, `technical_support`, `account_management`, `sales_inquiry`, `complaint`, `compliment`, `other`

---

## 6. Out of Scope

- Multilingual translation (inputs not in supported languages are rejected with HTTP 422).
- Generation or summarisation tasks.
- PII detection or redaction.
