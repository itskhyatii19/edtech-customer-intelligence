"""Analytics service for aggregations and insights"""

import pandas as pd
import streamlit as st
from .data_loader import DataLoader
from .cache_utils import make_cache_buster


class AnalyticsService:
    """Provides analytics aggregations and metrics"""

    @staticmethod
    @st.cache_data
    def _cached_engagement_metrics(cache_buster: str):
        df = DataLoader.load_features()
        if df is None:
            return {}

        if df.empty or "engagement_score" not in df.columns:
            return {
                "avg_engagement": 0.0,
                "median_engagement": 0.0,
                "total_activities": 0,
                "avg_activities_per_user": 0.0,
            }

        return {
            "avg_engagement": float(df["engagement_score"].mean()),
            "median_engagement": float(df["engagement_score"].median()),
            "total_activities": int(df["activity_count"].sum()),
            "avg_activities_per_user": float(df["activity_count"].mean()),
        }

    @staticmethod
    def get_engagement_metrics():
        token = make_cache_buster("analytics_engagement_metrics")
        return AnalyticsService._cached_engagement_metrics(token)

    @staticmethod
    @st.cache_data
    def _cached_retention_metrics(cache_buster: str):
        df = DataLoader.load_features()
        if df is None:
            return {}

        if df.empty or "inactive_days" not in df.columns:
            return {
                "active_users": 0,
                "inactive_users": 0,
                "active_percentage": 0.0,
                "avg_inactive_days": 0.0,
                "median_inactive_days": 0.0,
            }

        active_threshold = 30  # Days
        active_users = len(df[df["inactive_days"] <= active_threshold])
        inactive_users = len(df) - active_users

        return {
            "active_users": int(active_users),
            "inactive_users": int(inactive_users),
            "active_percentage": float(active_users / len(df) * 100),
            "avg_inactive_days": float(df["inactive_days"].mean()),
            "median_inactive_days": float(df["inactive_days"].median()),
        }

    @staticmethod
    def get_retention_metrics():
        token = make_cache_buster("analytics_retention_metrics")
        return AnalyticsService._cached_retention_metrics(token)

    @staticmethod
    @st.cache_data
    def _cached_churn_metrics(cache_buster: str):
        df = DataLoader.load_features()
        if df is None:
            return {}

        if df.empty or "churn_risk" not in df.columns:
            return {
                "high_risk_count": 0,
                "high_risk_percentage": 0.0,
                "low_risk_count": 0,
            }

        high_risk = len(df[df["churn_risk"] == "high"])
        total = len(df)

        return {
            "high_risk_count": int(high_risk),
            "high_risk_percentage": float(high_risk / total * 100),
            "low_risk_count": int(len(df[df["churn_risk"] == "low"])),
        }

    @staticmethod
    def get_churn_metrics():
        token = make_cache_buster("analytics_churn_metrics")
        return AnalyticsService._cached_churn_metrics(token)

    @staticmethod
    @st.cache_data
    def _cached_segment_comparison(cache_buster: str):
        df = DataLoader.load_features()
        if df is None:
            return None

        required_columns = {"user_segment", "uuid", "engagement_score", "activity_count", "inactive_days"}
        if df.empty or not required_columns.issubset(df.columns):
            return pd.DataFrame()

        segment_stats = (
            df.groupby("user_segment")
            .agg({
                "uuid": "count",
                "engagement_score": ["mean", "median"],
                "activity_count": ["mean", "sum"],
                "inactive_days": "mean",
            })
            .round(2)
        )
        segment_stats.columns = [
            "User Count",
            "Avg Engagement",
            "Median Engagement",
            "Avg Activity",
            "Total Activity",
            "Avg Inactive Days",
        ]
        return segment_stats

    @staticmethod
    def get_segment_comparison():
        token = make_cache_buster("analytics_segment_comparison")
        return AnalyticsService._cached_segment_comparison(token)

    @staticmethod
    @st.cache_data
    def _cached_top_reviewers(cache_buster: str, n: int):
        reviews = DataLoader.load_reviews()
        if reviews is None or "Reviewer" not in reviews.columns:
            return None

        top_reviewers = (
            reviews["Reviewer"].value_counts().head(n).reset_index()
        )
        top_reviewers.columns = ["Reviewer", "Review Count"]
        return top_reviewers

    @staticmethod
    def get_top_reviewers(n=10):
        token = make_cache_buster("analytics_top_reviewers")
        return AnalyticsService._cached_top_reviewers(token, n)

    @staticmethod
    @st.cache_data
    def _cached_engagement_distribution(cache_buster: str):
        df = DataLoader.load_features()
        if df is None:
            return {}

        if df.empty or "engagement_score" not in df.columns:
            return {}

        bins = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
        bin_labels = ["0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1.0"]

        distribution = pd.cut(
            df["engagement_score"],
            bins=bins,
            labels=bin_labels,
            right=False,
        ).value_counts().sort_index()

        return distribution.to_dict()

    @staticmethod
    def get_engagement_distribution():
        token = make_cache_buster("analytics_engagement_distribution")
        return AnalyticsService._cached_engagement_distribution(token)

    @staticmethod
    @st.cache_data
    def _cached_inactivity_distribution(cache_buster: str):
        df = DataLoader.load_features()
        if df is None:
            return {}

        if df.empty or "inactive_days" not in df.columns:
            return {}

        bins = [0, 30, 60, 90, 180, 365]
        bin_labels = ["0-30d", "30-60d", "60-90d", "90-180d", "180-365d"]

        distribution = pd.cut(
            df["inactive_days"],
            bins=bins,
            labels=bin_labels,
            right=False,
        ).value_counts().sort_index()

        return distribution.to_dict()

    @staticmethod
    def get_inactivity_distribution():
        token = make_cache_buster("analytics_inactivity_distribution")
        return AnalyticsService._cached_inactivity_distribution(token)

    @staticmethod
    @st.cache_data
    def _cached_review_statistics(cache_buster: str):
        reviews = DataLoader.load_reviews()
        if reviews is None:
            return {}

        if reviews.empty:
            return {
                "total_reviews": 0,
                "unique_reviewers": 0,
                "avg_rating": None,
                "median_rating": None,
            }

        stats = {
            "total_reviews": len(reviews),
            "unique_reviewers": reviews["Reviewer"].nunique() if "Reviewer" in reviews.columns else 0,
        }

        if "Rating" in reviews.columns:
            stats.update({
                "avg_rating": float(reviews["Rating"].mean()),
                "median_rating": float(reviews["Rating"].median()),
            })

        return stats

    @staticmethod
    def get_review_statistics():
        token = make_cache_buster("analytics_review_statistics")
        return AnalyticsService._cached_review_statistics(token)
