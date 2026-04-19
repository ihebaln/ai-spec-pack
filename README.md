# AI Spec Pack

Intent classification service — specs, data contracts, eval gate, and CI skeleton.

## Structure

```
specs/          — SRS, Acceptance Criteria, DataSpec, DataContract, ModelSpec, EvalPlan, Dataset Card
src/            — eval_gate.py
tests/          — pytest: data checks + general tests
data/           — dataset_v1.0.csv, golden_set.jsonl
reports/        — metrics.json (output of eval run)
configs/        — thresholds.yaml (eval gate config)
.github/workflows/ci.yml
```

## Commands

```bash
pip install -r requirements.txt

make test        # run all pytest tests
make data-check  # run data contract checks only
make eval-gate   # compare metrics.json to thresholds.yaml
```

## CI

GitHub Actions runs all three commands on every push to `main`.
