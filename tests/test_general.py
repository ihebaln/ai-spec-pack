"""
General tests — sanity checks on project structure and eval gate logic.
"""
import json
import yaml
import pytest
from pathlib import Path

ROOT = Path(__file__).parent.parent


def test_metrics_json_exists():
    assert (ROOT / "reports" / "metrics.json").exists()


def test_thresholds_yaml_exists():
    assert (ROOT / "configs" / "thresholds.yaml").exists()


def test_golden_set_exists():
    assert (ROOT / "data" / "golden_set.jsonl").exists()


def test_golden_set_has_30_examples():
    lines = (ROOT / "data" / "golden_set.jsonl").read_text().strip().splitlines()
    assert len(lines) == 30, f"Expected 30 golden set examples, got {len(lines)}"


def test_metrics_json_valid():
    with open(ROOT / "reports" / "metrics.json") as f:
        data = json.load(f)
    assert "macro_f1" in data
    assert "accuracy" in data


def test_thresholds_yaml_valid():
    with open(ROOT / "configs" / "thresholds.yaml") as f:
        data = yaml.safe_load(f)
    assert "thresholds" in data
    assert "macro_f1" in data["thresholds"]


def test_eval_gate_passes_with_stub_metrics():
    """Verify the stub metrics.json passes all gates."""
    import subprocess, sys
    result = subprocess.run(
        [sys.executable, str(ROOT / "src" / "eval_gate.py")],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Eval gate failed:\n{result.stdout}\n{result.stderr}"
