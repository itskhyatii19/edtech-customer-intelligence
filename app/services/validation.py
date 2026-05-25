from __future__ import annotations

import pandas as pd
from typing import Iterable, Mapping


class ValidationError(Exception):
    """Raised when DataFrame validation rules fail."""


def sanitize_dataframe(df: pd.DataFrame | None) -> pd.DataFrame:
    if df is None:
        return pd.DataFrame()
    if not isinstance(df, pd.DataFrame):
        raise ValidationError("Expected a pandas DataFrame object.")
    return df.copy()


def validate_required_columns(df: pd.DataFrame, required_columns: Iterable[str]) -> bool:
    df = sanitize_dataframe(df)
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValidationError(f"Missing required columns: {', '.join(missing)}")
    return True


def validate_numeric_columns(df: pd.DataFrame, numeric_columns: Iterable[str]) -> bool:
    df = sanitize_dataframe(df)
    invalid = [
        col
        for col in numeric_columns
        if col in df.columns and not pd.api.types.is_numeric_dtype(df[col])
    ]
    if invalid:
        raise ValidationError(
            f"Expected numeric columns but found non-numeric: {', '.join(invalid)}"
        )
    return True


def validate_no_null_threshold(df: pd.DataFrame, threshold: float = 0.2) -> bool:
    df = sanitize_dataframe(df)
    if not 0 <= threshold <= 1:
        raise ValidationError("Null threshold must be between 0 and 1.")
    null_share = df.isna().mean()
    bad_columns = null_share[null_share > threshold].index.tolist()
    if bad_columns:
        raise ValidationError(
            f"Columns exceed null threshold ({threshold * 100:.0f}%): {', '.join(bad_columns)}"
        )
    return True
