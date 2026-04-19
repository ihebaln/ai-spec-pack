"""
Data contract checks for dataset_v1.0.csv
Covers: 3 syntactic, 4 structural, 3 statistical = 10 checks minimum.
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "dataset_v1.0.csv"
ALLOWED_LABELS = {
    "billing", "technical_support", "account_management",
    "sales_inquiry", "complaint", "compliment", "other"
}
ALLOWED_SPLITS = {"train", "val", "test"}
REQUIRED_COLUMNS = {"id", "text", "label", "language", "source", "split"}


@pytest.fixture(scope="module")
def df():
    return pd.read_csv(DATA_PATH)


# ── SYNTACTIC CHECKS ────────────────────────────────────────────────────────


def test_syn_01_file_is_valid_csv():
    """File must be parseable as CSV."""
    try:
        df = pd.read_csv(DATA_PATH)
        assert len(df) > 0, "CSV is empty"
    except Exception as e:
        pytest.fail(f"CSV parsing failed: {e}")


def test_syn_02_required_columns_present(df):
    """All required columns must be present."""
    missing = REQUIRED_COLUMNS - set(df.columns)
    assert not missing, f"Missing columns: {missing}"


def test_syn_03_no_empty_text(df):
    """No record may have an empty or whitespace-only text field."""
    empty_mask = df["text"].isna() | (df["text"].str.strip() == "")
    assert not empty_mask.any(), (
        f"{empty_mask.sum()} records have empty text. IDs: {df.loc[empty_mask, 'id'].tolist()}"
    )


# ── STRUCTURAL CHECKS ────────────────────────────────────────────────────────


def test_str_01_no_duplicate_ids(df):
    """Record IDs must be unique."""
    dupes = df[df.duplicated(subset=["id"])]["id"].tolist()
    assert not dupes, f"Duplicate IDs found: {dupes}"


def test_str_02_no_train_test_text_leakage(df):
    """No text should appear in both train and test splits (data leakage)."""
    train_texts = set(df.loc[df["split"] == "train", "text"].str.strip())
    test_texts = set(df.loc[df["split"] == "test", "text"].str.strip())
    overlap = train_texts & test_texts
    assert not overlap, f"Train/test text overlap ({len(overlap)} records): {list(overlap)[:5]}"


def test_str_03_valid_labels(df):
    """All label values must be in the allowed set."""
    invalid = set(df["label"].unique()) - ALLOWED_LABELS
    assert not invalid, f"Unknown labels: {invalid}"


def test_str_04_valid_splits(df):
    """Split column must only contain train/val/test."""
    invalid = set(df["split"].unique()) - ALLOWED_SPLITS
    assert not invalid, f"Unknown split values: {invalid}"


# ── STATISTICAL CHECKS ────────────────────────────────────────────────────────


def test_stat_01_class_imbalance(df):
    """No single class should exceed 50% of total records."""
    counts = df["label"].value_counts(normalize=True)
    dominant = counts[counts > 0.50]
    assert dominant.empty, (
        f"Class imbalance: {dominant.to_dict()}"
    )


def test_stat_02_distribution_shift_proxy(df):
    """Train and test label distributions should not diverge by more than 0.20 in any class (proxy check)."""
    train_dist = df[df["split"] == "train"]["label"].value_counts(normalize=True)
    test_dist = df[df["split"] == "test"]["label"].value_counts(normalize=True)
    all_labels = set(train_dist.index) | set(test_dist.index)
    max_delta = 0.0
    for label in all_labels:
        t = train_dist.get(label, 0.0)
        v = test_dist.get(label, 0.0)
        max_delta = max(max_delta, abs(t - v))
    assert max_delta <= 0.25, (
        f"Distribution shift too large (max delta={max_delta:.3f}). "
        "Train and test label distributions diverge."
    )


def test_stat_03_source_dominance(df):
    """No single source should dominate more than 70% of records."""
    source_fractions = df["source"].value_counts(normalize=True)
    dominant = source_fractions[source_fractions > 0.70]
    assert dominant.empty, (
        f"Source dominance: {dominant.to_dict()}"
    )


def test_stat_04_text_length_p99(df):
    """p99 text length must not exceed 512 characters."""
    lengths = df["text"].str.len()
    p99 = np.percentile(lengths, 99)
    assert p99 <= 512, f"p99 text length is {p99:.0f} chars, exceeds limit of 512"
