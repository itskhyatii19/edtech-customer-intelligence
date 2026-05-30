"""Dashboard pages module."""

from .ai_insights import render as render_ai_insights
from .home import render as render_home
from .learner_analytics import render as render_learner_analytics
from .predictive_analytics import render as render_predictive_analytics
from .review_intelligence import render as render_review_intelligence
from .settings import render as render_settings

__all__ = [
    "render_home",
    "render_ai_insights",
    "render_learner_analytics",
    "render_predictive_analytics",
    "render_review_intelligence",
    "render_settings",
]
