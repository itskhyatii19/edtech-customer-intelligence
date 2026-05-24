"""Deterministic insight generation for AI Insights page.

This service provides simple, rule-based business signals that can later
be augmented with LLM-based explanations or more advanced anomaly detection.
"""
from typing import Dict, Any

import pandas as pd

from .data_loader import DataLoader
from .logger import get_logger


class InsightService:
    logger = get_logger(__name__)

    @staticmethod
    def generate_insights(sample_n: int = 10) -> Dict[str, Any]:
        df = DataLoader.load_features()

        if df is None or df.empty:
            return {
                "summary": pd.DataFrame(
                    [
                        {"metric": "total_users", "value": 0},
                        {"metric": "avg_engagement", "value": 0.0},
                        {"metric": "high_risk_pct", "value": 0.0},
                        {"metric": "avg_churn_probability", "value": 0.0},
                        {"metric": "critical_risk_pct", "value": 0.0},
                    ]
                ),
                "churn_anomalies": pd.DataFrame(),
                "engagement_drop_candidates": pd.DataFrame(),
                "at_risk_segments": pd.DataFrame(),
            }

        # Basic aggregates
        total_users = len(df)
        avg_engagement = float(df.get("engagement_score", pd.Series([0])).mean())
        high_risk_pct = float((df.get("churn_risk", pd.Series(dtype=object)) == "high").mean())
        churn_prob = float(df["churn_probability"].mean()) if "churn_probability" in df.columns else 0.0
        critical_pct = float((df.get("churn_probability", 0) >= 0.8).mean()) if "churn_probability" in df.columns else 0.0

        # Churn anomalies: extreme scores
        churn_anomalies = df[df.get("churn_score", 0) >= 0.9]
        churn_anomalies_sample = churn_anomalies.head(sample_n)

        # Engagement drop candidates: low engagement and long inactive
        candidates = df[
            (df.get("engagement_score", 1) < 0.3)
            & (
                df.get("inactive_days", 999) > 30
            )
        ]
        candidates_sample = candidates.head(sample_n)

        # Top at-risk segments (by churn_risk or segment column if present)
        segment_key = "user_segment" if "user_segment" in df.columns else "segment" if "segment" in df.columns else None
        if segment_key:
            at_risk_segments = (
                df.groupby(segment_key)
                .agg({"churn_score": "mean", "uuid": "count"})
                .sort_values("churn_score", ascending=False)
                .reset_index()
            )
        elif "churn_risk" in df.columns:
            at_risk_segments = (
                df.groupby("churn_risk")
                .agg({"churn_score": "mean", "uuid": "count"})
                .sort_values("churn_score", ascending=False)
                .reset_index()
            )
        else:
            at_risk_segments = pd.DataFrame()

        summary = pd.DataFrame(
            [
                {"metric": "total_users", "value": total_users},
                {"metric": "avg_engagement", "value": avg_engagement},
                {"metric": "high_risk_pct", "value": high_risk_pct},
                {"metric": "avg_churn_probability", "value": churn_prob},
                {"metric": "critical_risk_pct", "value": critical_pct},
            ]
        )

        return {
            "summary": summary,
            "churn_anomalies": churn_anomalies_sample,
            "engagement_drop_candidates": candidates_sample,
            "at_risk_segments": at_risk_segments,
        }
