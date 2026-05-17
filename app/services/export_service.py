"""Export utilities for downloading data as CSV."""

import io
import pandas as pd
from typing import Optional


def df_to_csv_bytes(df: pd.DataFrame, index: bool = False) -> bytes:
    """Convert DataFrame to CSV bytes suitable for Streamlit `download_button`."""
    buffer = io.StringIO()
    df.to_csv(buffer, index=index)
    return buffer.getvalue().encode("utf-8")


def save_df_to_path(df: pd.DataFrame, path: str, index: bool = False) -> None:
    """Save DataFrame to a CSV file path on disk."""
    df.to_csv(path, index=index)


def get_filtered_reviews_csv(filtered_df: pd.DataFrame) -> Optional[bytes]:
    if filtered_df is None or filtered_df.empty:
        return None
    return df_to_csv_bytes(filtered_df)
