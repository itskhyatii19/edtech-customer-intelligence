"""Deterministic recommendation engine for interventions."""
from __future__ import annotations

from typing import Dict, Any

import pandas as pd

from app.services.logger import get_logger

logger = get_logger(__name__)


class RecommendationService:
    @staticmethod
    def recommend(df: pd.DataFrame, churn_prob_col: str = "churn_probability") -> pd.DataFrame:
        if df is None or df.empty or churn_prob_col not in df.columns:
            return pd.DataFrame()

        out = df.copy()
        out["recommendation"] = ""
        out["recommendation_severity"] = "low"

        # High priority: high churn prob + inactivity + negative sentiment
        mask = (out[churn_prob_col] >= 0.75) | (out.get("churn_score", 0) >= 0.75)
        out.loc[mask & (out.get("review_sentiment_score", 0) <= -0.2), "recommendation"] = "Re-engagement + Instructor follow-up"
        out.loc[mask & (out.get("review_sentiment_score", 0) > -0.2), "recommendation"] = "Re-engagement campaign"
        out.loc[mask, "recommendation_severity"] = "high"

        # Medium priority
        mask2 = (out[churn_prob_col] >= 0.5) & (out[churn_prob_col] < 0.75)
        out.loc[mask2, "recommendation"] = "Nudge messages + content suggestions"
        out.loc[mask2, "recommendation_severity"] = "medium"

        # Low priority
        mask3 = out[churn_prob_col] < 0.5
        out.loc[mask3 & (out.get("activity_trend", 0) > 0.1), "recommendation"] = "Upsell / advanced content targeting"
        out.loc[mask3 & (out.get("activity_trend", 0) <= 0.1), "recommendation"] = "Monitor"

        return out[["uuid", churn_prob_col, "recommendation", "recommendation_severity"]].copy()
