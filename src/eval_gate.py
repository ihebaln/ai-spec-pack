"""
eval_gate.py
Compares reports/metrics.json against configs/thresholds.yaml.
Exits 0 if all gates pass, 1 if any gate fails.
"""
import json
import sys
import yaml
from pathlib import Path

ROOT = Path(__file__).parent.parent
METRICS_PATH = ROOT / "reports" / "metrics.json"
THRESHOLDS_PATH = ROOT / "configs" / "thresholds.yaml"


def load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def load_yaml(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def check_gates(metrics: dict, thresholds: dict) -> list[str]:
    failures = []
    gate_defs = thresholds.get("thresholds", {})

    for metric_name, bounds in gate_defs.items():
        if metric_name not in metrics:
            failures.append(f"MISSING metric '{metric_name}' in metrics.json")
            continue

        value = metrics[metric_name]

        if "min" in bounds and value < bounds["min"]:
            failures.append(
                f"FAIL  {metric_name} = {value:.4f}  <  min {bounds['min']}"
            )
        elif "max" in bounds and value > bounds["max"]:
            failures.append(
                f"FAIL  {metric_name} = {value:.4f}  >  max {bounds['max']}"
            )
        else:
            bound_desc = f"min={bounds.get('min')}  max={bounds.get('max')}"
            print(f"PASS  {metric_name} = {value}  ({bound_desc})")

    return failures


def main():
    print(f"Loading metrics from  : {METRICS_PATH}")
    print(f"Loading thresholds from: {THRESHOLDS_PATH}\n")

    metrics = load_json(METRICS_PATH)
    thresholds = load_yaml(THRESHOLDS_PATH)

    failures = check_gates(metrics, thresholds)

    print()
    if failures:
        print("=" * 60)
        print("EVAL GATE FAILED — the following checks did not pass:")
        for f in failures:
            print(f"  {f}")
        print("=" * 60)
        sys.exit(1)
    else:
        print("=" * 60)
        print("EVAL GATE PASSED — all thresholds met.")
        print("=" * 60)
        sys.exit(0)


if __name__ == "__main__":
    main()
