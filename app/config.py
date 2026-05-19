"""Application configuration and constants"""

import os
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# Data paths
DATA_DIR = PROJECT_ROOT / "data"
JUNYI_DATA_DIR = DATA_DIR / "junyi" / "raw"
REVIEWS_DATA_DIR = DATA_DIR / "reviews" / "raw"

# File paths
USERS_CSV = JUNYI_DATA_DIR / "Info_UserData.csv"
LOGS_CSV = JUNYI_DATA_DIR / "Log_Problem.csv"
REVIEWS_CSV = REVIEWS_DATA_DIR / "reviews.csv"
REVIEWS_BY_COURSE_CSV = REVIEWS_DATA_DIR / "reviews_by_course.csv"

# Feature engineering thresholds
ENGAGEMENT_HIGH_THRESHOLD = 0.7
ENGAGEMENT_MODERATE_THRESHOLD = 0.3
CHURN_ENGAGEMENT_QUANTILE = 0.3
CHURN_INACTIVITY_QUANTILE = 0.7
MAX_INACTIVE_DAYS = 365

# Data loading limits
LOG_ROWS_LIMIT = 500000

# App configuration
APP_TITLE = "EdTech Customer Intelligence Platform"
APP_DESCRIPTION = "AI-powered analytics for student engagement and success"
APP_ICON = "📊"
APP_VERSION = "0.1.0"
APP_AUTHOR = "EdTech Analytics Team"
APP_COPYRIGHT = "© 2026 EdTech Customer Intelligence"
APP_PAGES = ["Overview", "Learner Analytics", "AI Insights", "Review Intelligence", "Settings"]

# Color scheme
COLORS = {
    "primary": "#1f77b4",
    "secondary": "#ff7f0e",
    "success": "#2ca02c",
    "warning": "#d62728",
    "neutral": "#7f7f7f",
}

# Engagement segments
SEGMENTS = {
    "highly_active": {"label": "Highly Active", "color": COLORS["success"]},
    "moderate": {"label": "Moderate", "color": COLORS["secondary"]},
    "low_active": {"label": "Low Active", "color": COLORS["warning"]},
}

# Churn risk levels
CHURN_RISK_COLORS = {
    "low": "#2ca02c",
    "medium": "#ff7f0e",
    "high": "#d62728",
}
