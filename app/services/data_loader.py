"""Data loading and caching service"""

import pandas as pd
import streamlit as st
from pathlib import Path
import sys
import os

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.features.build_features import (
    load_data as load_raw_data,
    create_engagement,
    create_inactivity,
    merge_features,
    segment_users,
)
from app.services.churn_service import ChurnService
from app.config import (
    USERS_CSV,
    LOGS_CSV,
    REVIEWS_CSV,
    LOG_ROWS_LIMIT,
)


class DataLoader:
    """Handles data loading with Streamlit caching"""

    @staticmethod
    @st.cache_data(ttl=3600)  # Cache for 1 hour
    def load_users_and_logs():
        """Load user and activity log data from CSV files"""
        try:
            users = pd.read_csv(USERS_CSV)
            logs = pd.read_csv(LOGS_CSV, nrows=LOG_ROWS_LIMIT)
            return users, logs
        except FileNotFoundError as e:
            st.error(f"Data file not found: {e}")
            return None, None

    @staticmethod
    @st.cache_data(ttl=3600)
    def load_reviews():
        """Load reviews data from CSV"""
        try:
            reviews = pd.read_csv(REVIEWS_CSV)
            return reviews
        except FileNotFoundError as e:
            st.error(f"Reviews file not found: {e}")
            return None

    @staticmethod
    @st.cache_data(ttl=3600)
    def load_features():
        """
        Load and compute all features (engagement, inactivity, churn, segments)
        
        Returns:
            DataFrame with computed features for all users
        """
        users, logs = DataLoader.load_users_and_logs()
        
        if users is None or logs is None:
            return None

        # Build feature pipeline
        # Ensure timestamps are parsed for activity frequency calculations
        if "timestamp_TW" in logs.columns:
            logs = logs.copy()
            logs["timestamp_TW"] = pd.to_datetime(logs["timestamp_TW"], errors="coerce")

        engagement = create_engagement(logs)
        inactivity = create_inactivity(logs)

        # Compute days_active per user for frequency normalization
        if "timestamp_TW" in logs.columns:
            span = logs.groupby("uuid")["timestamp_TW"].agg(["min", "max"]).reset_index()
            span["days_active"] = (span["max"] - span["min"]).dt.days + 1
            span = span[["uuid", "days_active"]]
        else:
            span = pd.DataFrame({"uuid": engagement["uuid"].unique(), "days_active": 1})

        df = merge_features(users, engagement, inactivity)

        # Merge days_active and activity_count into features
        df = df.merge(span, on="uuid", how="left")
        df["days_active"] = df["days_active"].fillna(1).astype(int)

        # Compute improved churn scores and bands using ChurnService
        df = ChurnService.compute_and_assign(df)

        # Keep segmentation
        df = segment_users(df)

        return df

    @staticmethod
    def get_user_count():
        """Get total number of users"""
        df = DataLoader.load_features()
        return len(df) if df is not None else 0

    @staticmethod
    def get_review_count():
        """Get total number of reviews"""
        reviews = DataLoader.load_reviews()
        return len(reviews) if reviews is not None else 0

    @staticmethod
    def get_segment_counts():
        """Get user count by engagement segment"""
        df = DataLoader.load_features()
        if df is None:
            return {}
        return df["user_segment"].value_counts().to_dict()

    @staticmethod
    def get_churn_distribution():
        """Get distribution of churn risk"""
        df = DataLoader.load_features()
        if df is None:
            return {}
        return df["churn_risk"].value_counts().to_dict()
