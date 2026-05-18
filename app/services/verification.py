"""Lightweight developer health-check utilities.

This module provides fast verification helpers for cache behavior, import health,
service class availability, and lightweight data loading. It avoids expensive
feature computations and analytics pipelines.
"""

from typing import Any, Dict

from .cache_utils import verify_cache_helpers
from .data_loader import DataLoader
from .analytics_service import AnalyticsService
from .review_service import ReviewService
from .churn_service import ChurnService
from .insight_service import InsightService


def verify_imports() -> Dict[str, Any]:
    """Verify core service modules can be imported."""
    checks: Dict[str, Any] = {}
    modules = {
        "cache_utils": "app.services.cache_utils",
        "data_loader": "app.services.data_loader",
        "analytics_service": "app.services.analytics_service",
        "review_service": "app.services.review_service",
        "churn_service": "app.services.churn_service",
        "insight_service": "app.services.insight_service",
    }

    for label, module_name in modules.items():
        try:
            __import__(module_name)
            checks[label] = {"pass": True}
        except Exception as exc:  # noqa: BLE001
            checks[label] = {"pass": False, "error": str(exc)}

    return {
        "pass": all(item["pass"] for item in checks.values()),
        "details": checks,
    }


def verify_services() -> Dict[str, Any]:
    """Verify core service classes expose expected lightweight APIs."""
    checks: Dict[str, Any] = {
        "DataLoader.load_users_and_logs": hasattr(DataLoader, "load_users_and_logs"),
        "DataLoader.load_reviews": hasattr(DataLoader, "load_reviews"),
        "DataLoader.verify_light_loads": hasattr(DataLoader, "verify_light_loads"),
        "AnalyticsService.get_engagement_metrics": hasattr(AnalyticsService, "get_engagement_metrics"),
        "AnalyticsService.get_retention_metrics": hasattr(AnalyticsService, "get_retention_metrics"),
        "ReviewService.filter_reviews": hasattr(ReviewService, "filter_reviews"),
        "ReviewService.get_top_keywords": hasattr(ReviewService, "get_top_keywords"),
        "ChurnService.compute_and_assign": hasattr(ChurnService, "compute_and_assign"),
        "InsightService.generate_insights": hasattr(InsightService, "generate_insights"),
    }

    return {
        "pass": all(checks.values()),
        "details": {key: {"pass": bool(value)} for key, value in checks.items()},
    }


def run_all_checks() -> Dict[str, Any]:
    """Run all lightweight verification checks and return a structured summary."""
    cache_result = verify_cache_helpers()
    light_loads_result = DataLoader.verify_light_loads()
    imports_result = verify_imports()
    services_result = verify_services()

    summary = {
        "cache": cache_result["pass"],
        "light_loads": (
            bool(light_loads_result.get("users_loaded"))
            and bool(light_loads_result.get("logs_loaded"))
            and bool(light_loads_result.get("reviews_loaded"))
        ),
        "imports": imports_result["pass"],
        "services": services_result["pass"],
    }

    return {
        "pass": all(summary.values()),
        "summary": summary,
        "cache": cache_result,
        "light_loads": light_loads_result,
        "imports": imports_result,
        "services": services_result,
    }
