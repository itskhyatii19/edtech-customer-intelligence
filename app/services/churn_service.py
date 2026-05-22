"""Churn scoring service: computes weighted churn score and assigns risk bands."""

from typing import Dict, Iterable

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from app.config import MAX_INACTIVE_DAYS
from app.services.logger import get_logger
from app.services.validation import ValidationError, validate_numeric_columns, validate_required_columns


class ChurnService:
    """Provides churn scoring utilities.

    Score combines engagement_score (higher is better), inactive_days (higher is worse),
    and activity_frequency (higher is better). The resulting score is normalized to [0,1]
    where higher values indicate higher churn risk.
    """

    @staticmethod
    def _safe_div(a, b):
        return a / b if b != 0 else 0

    @staticmethod
    def _build_ml_features(df: pd.DataFrame) -> pd.DataFrame:
        required = ["engagement_score", "inactive_days", "activity_count", "days_active"]
        validate_required_columns(df, required)
        validate_numeric_columns(df, ["engagement_score", "inactive_days", "activity_count", "days_active"])

        features = df[required].copy()
        features["days_active"] = features["days_active"].replace(0, 1).fillna(1)
        features["activity_per_day"] = features["activity_count"] / features["days_active"]
        features = features.fillna(0)
        return features[["engagement_score", "inactive_days", "activity_count", "activity_per_day"]]

    @staticmethod
    def _build_target(df: pd.DataFrame) -> pd.Series:
        if "churn_risk" not in df.columns:
            raise ValidationError("Missing churn_risk target for model training.")
        return (df["churn_risk"] == "high").astype(int)

    @staticmethod
    def _get_model_pipeline() -> Pipeline:
        return Pipeline(
            [
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    LogisticRegression(max_iter=500, random_state=42, solver="liblinear"),
                ),
            ]
        )

    @staticmethod
    def train_churn_model(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42) -> Dict[str, object]:
        logger = get_logger(__name__)
        work = df.copy()
        if work is None or work.empty:
            raise ValidationError("Training data is empty.")

        X = ChurnService._build_ml_features(work)
        y = ChurnService._build_target(work)

        if y.nunique() < 2:
            raise ValidationError("Need at least two churn classes for model training.")

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        pipeline = ChurnService._get_model_pipeline()
        pipeline.fit(X_train, y_train)

        y_pred = pipeline.predict(X_test)
        y_prob = pipeline.predict_proba(X_test)[:, 1]
        accuracy = float(accuracy_score(y_test, y_pred))
        auc = float(roc_auc_score(y_test, y_prob)) if len(np.unique(y_test)) > 1 else 0.0

        feature_names = X.columns.tolist()
        coefficients = pipeline.named_steps["classifier"].coef_[0]
        importance = pd.DataFrame(
            {"feature": feature_names, "coefficient": coefficients}
        ).assign(abs_coef=lambda d: d["coefficient"].abs()).sort_values(
            "abs_coef", ascending=False
        )

        logger.info("Trained churn model: accuracy=%.3f auc=%.3f", accuracy, auc)
        return {
            "pipeline": pipeline,
            "accuracy": accuracy,
            "auc": auc,
            "importance": importance,
        }

    @staticmethod
    def predict_churn_probability(df: pd.DataFrame, model: Pipeline | None = None) -> pd.Series:
        work = df.copy()
        if model is None:
            raise ValidationError("No churn model provided for probability prediction.")

        features = ChurnService._build_ml_features(work)
        probs = model.predict_proba(features)[:, 1]
        return pd.Series(probs, index=work.index)

    @staticmethod
    def get_model_driver_summary(importance: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
        if importance is None or importance.empty:
            return pd.DataFrame()
        return importance.head(top_n).reset_index(drop=True)

    @staticmethod
    @st.cache_data(ttl=3600)
    def compute_churn_scores(df: pd.DataFrame,
                             weight_engagement: float = 0.5,
                             weight_inactivity: float = 0.3,
                             weight_frequency: float = 0.2,
                             max_inactive_days: int = MAX_INACTIVE_DAYS) -> pd.Series:
        """Compute a churn score for each user in `df`.

        Args:
            df: DataFrame with columns `uuid`, `engagement_score`, `inactive_days`, `activity_count`, `days_active`
            weights: importance weights for components
            max_inactive_days: cap for inactive days normalization

        Returns:
            pd.Series of churn scores between 0 and 1 (higher => higher risk)
        """
        # Ensure required columns exist
        required = ["engagement_score", "inactive_days", "activity_count"]
        for c in required:
            if c not in df.columns:
                raise ValueError(f"Missing required column for churn scoring: {c}")

        # Prepare working copy
        work = df.copy()

        # Normalize engagement: higher engagement -> lower risk
        eng = work["engagement_score"].fillna(0).clip(0, 1)
        eng_risk = 1 - eng  # higher when engagement low

        # Normalize inactivity: scale 0..max_inactive_days
        inactive = work["inactive_days"].fillna(max_inactive_days).clip(0, max_inactive_days)
        inactive_norm = inactive / max_inactive_days

        # Normalize activity frequency: activity_count / days_active (per day), then scale
        # days_active may be absent; we expect a `days_active` column added upstream.
        if "days_active" in work.columns and work["days_active"].notna().any():
            days_active = work["days_active"].replace(0, 1).fillna(1)
            freq = work["activity_count"] / days_active  # activities per day
        else:
            # fallback: use activity_count directly (relative)
            freq = work["activity_count"].fillna(0)

        # Scale frequency to 0..1 using robust scaling (cap at 95th percentile)
        cap = np.percentile(np.clip(freq, 0, None), 95) if len(freq) > 0 else 1
        cap = cap if cap > 0 else 1
        freq_norm = (freq / cap).clip(0, 1)
        freq_risk = 1 - freq_norm  # higher when frequency low

        # Weighted sum
        score = (weight_engagement * eng_risk) + (weight_inactivity * inactive_norm) + (weight_frequency * freq_risk)

        # Normalize score to 0..1
        score = (score - score.min()) / (score.max() - score.min() + 1e-9)

        return pd.Series(score, index=work.index)

    @staticmethod
    def assign_risk_band(scores: pd.Series, low_thresh: float = 0.33, high_thresh: float = 0.66) -> pd.Series:
        """Assign risk bands 'low', 'medium', 'high' from score series.

        Args:
            scores: Series of churn scores in [0,1]
            low_thresh: upper bound for 'low' risk
            high_thresh: upper bound for 'medium' risk

        Returns:
            Series of categorical risk labels
        """
        bands = pd.Series(index=scores.index, dtype=object)
        bands.loc[scores <= low_thresh] = "low"
        bands.loc[(scores > low_thresh) & (scores <= high_thresh)] = "medium"
        bands.loc[scores > high_thresh] = "high"
        return bands

    @staticmethod
    @st.cache_data(ttl=3600)
    def compute_and_assign(df: pd.DataFrame, low_thresh: float = 0.33, high_thresh: float = 0.66, **kwargs) -> pd.DataFrame:
        """Compute churn scores and assign bands; returns DataFrame with `churn_score` and `churn_risk`.

        This function is cached for 1 hour and is safe to call repeatedly from the app.
        """
        work = df.copy()
        scores = ChurnService.compute_churn_scores(work, **kwargs)
        work["churn_score"] = scores
        work["churn_risk"] = ChurnService.assign_risk_band(scores, low_thresh=low_thresh, high_thresh=high_thresh)
        try:
            model_meta = ChurnService.train_churn_model(work)
            work["churn_probability"] = ChurnService.predict_churn_probability(work, model_meta["pipeline"])
        except ValidationError:
            work["churn_probability"] = work["churn_score"]
        except Exception:
            work["churn_probability"] = work["churn_score"]
        return work
