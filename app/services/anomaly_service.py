"""Anomaly detection utilities for engagement and reviews.

Lightweight, defensive implementation using IsolationForest when available,
otherwise statistical thresholds.
"""
from __future__ import annotations

import logging
from typing import Dict, Any

import pandas as pd

try:
    from sklearn.ensemble import IsolationForest
    SKLEARN_AVAILABLE = True
except Exception:
    SKLEARN_AVAILABLE = False

from app.services.logger import get_logger

logger = get_logger(__name__)


class AnomalyService:
    @staticmethod
    def detect_engagement_anomalies(df: pd.DataFrame, score_col: str = "engagement_score") -> pd.DataFrame:
        if df is None or df.empty or score_col not in df.columns:
            return pd.DataFrame()

        work = df[[score_col]].fillna(0)
        if SKLEARN_AVAILABLE:
            iso = IsolationForest(n_estimators=100, contamination=0.02, random_state=42)
            preds = iso.fit_predict(work)
            anomalies = df[preds == -1]
            anomalies = anomalies.assign(anomaly_severity=(1 - anomalies[score_col]))
            return anomalies.sort_values("anomaly_severity", ascending=False)

        # Fallback: statistical cutoff (z-score-like)
        mean = work[score_col].mean()
        std = work[score_col].std() or 1
        cutoff = mean - 2 * std
        anomalies = df[df[score_col] < cutoff].copy()
        anomalies["anomaly_severity"] = (cutoff - anomalies[score_col]) / (std + 1e-9)
        return anomalies.sort_values("anomaly_severity", ascending=False)

    @staticmethod
    def detect_inactivity_spikes(df: pd.DataFrame, days_col: str = "inactive_days") -> pd.DataFrame:
        if df is None or df.empty or days_col not in df.columns:
            return pd.DataFrame()
        q95 = df[days_col].quantile(0.95)
        spikes = df[df[days_col] >= q95].copy()
        spikes["severity"] = (spikes[days_col] - q95) / (q95 + 1e-9)
        return spikes.sort_values("severity", ascending=False)
