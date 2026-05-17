"""Analytics service for aggregations and insights"""

import pandas as pd
import streamlit as st
from .data_loader import DataLoader


class AnalyticsService:
    """Provides analytics aggregations and metrics"""

    @staticmethod
    @st.cache_data(ttl=3600)
    def get_engagement_metrics():
        """
        Calculate overall engagement metrics
        
        Returns:
            dict: Contains avg_engagement, median_engagement, total_activities
        """
        df = DataLoader.load_features()
        if df is None:
            return {}

        return {
            "avg_engagement": float(df["engagement_score"].mean()),
            "median_engagement": float(df["engagement_score"].median()),
            "total_activities": int(df["activity_count"].sum()),
            "avg_activities_per_user": float(df["activity_count"].mean()),
        }

    @staticmethod
    @st.cache_data(ttl=3600)
    def get_retention_metrics():
        """
        Calculate retention and inactivity metrics
        
        Returns:
            dict: Contains active_users, inactive_users, avg_inactive_days
        """
        df = DataLoader.load_features()
        if df is None:
            return {}

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
    @st.cache_data(ttl=3600)
    def get_churn_metrics():
        """
        Calculate churn risk metrics
        
        Returns:
            dict: Contains high_risk_count, high_risk_percentage
        """
        df = DataLoader.load_features()
        if df is None:
            return {}

        high_risk = len(df[df["churn_risk"] == "high"])
        total = len(df)

        return {
            "high_risk_count": int(high_risk),
            "high_risk_percentage": float(high_risk / total * 100),
            "low_risk_count": int(len(df[df["churn_risk"] == "low"])),
        }

    @staticmethod
    @st.cache_data(ttl=3600)
    def get_segment_comparison():
        """
        Get metrics grouped by user segment
        
        Returns:
            DataFrame: Segment statistics (count, avg engagement, avg activity)
        """
        df = DataLoader.load_features()
        if df is None:
            return None

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
    @st.cache_data(ttl=3600)
    def get_top_reviewers(n=10):
        """
        Get top reviewers by number of reviews
        
        Args:
            n: Number of top reviewers to return
            
        Returns:
            DataFrame: Top reviewers with review counts
        """
        reviews = DataLoader.load_reviews()
        if reviews is None or "Reviewer" not in reviews.columns:
            return None

        top_reviewers = (
            reviews["Reviewer"].value_counts().head(n).reset_index()
        )
        top_reviewers.columns = ["Reviewer", "Review Count"]
        return top_reviewers

    @staticmethod
    @st.cache_data(ttl=3600)
    def get_engagement_distribution():
        """
        Get binned distribution of engagement scores
        
        Returns:
            dict: Engagement score distribution
        """
        df = DataLoader.load_features()
        if df is None:
            return {}

        # Create bins for engagement
        bins = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
        bin_labels = ["0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1.0"]
        
        distribution = pd.cut(
            df["engagement_score"],
            bins=bins,
            labels=bin_labels,
            right=False
        ).value_counts().sort_index()

        return distribution.to_dict()

    @staticmethod
    @st.cache_data(ttl=3600)
    def get_inactivity_distribution():
        """
        Get binned distribution of inactivity days
        
        Returns:
            dict: Inactivity days distribution
        """
        df = DataLoader.load_features()
        if df is None:
            return {}

        bins = [0, 30, 60, 90, 180, 365]
        bin_labels = ["0-30d", "30-60d", "60-90d", "90-180d", "180-365d"]
        
        distribution = pd.cut(
            df["inactive_days"],
            bins=bins,
            labels=bin_labels,
            right=False
        ).value_counts().sort_index()

        return distribution.to_dict()

    @staticmethod
    @st.cache_data(ttl=3600)
    def get_review_statistics():
        """
        Get review count and basic statistics
        
        Returns:
            dict: Review count, avg rating, etc.
        """
        reviews = DataLoader.load_reviews()
        if reviews is None:
            return {}

        stats = {
            "total_reviews": len(reviews),
            "unique_reviewers": reviews["Reviewer"].nunique() if "Reviewer" in reviews.columns else 0,
        }

        # Add rating stats if Rating column exists
        if "Rating" in reviews.columns:
            stats.update({
                "avg_rating": float(reviews["Rating"].mean()),
                "median_rating": float(reviews["Rating"].median()),
            })

        return stats
