"""Learner Analytics page proxy for the production-style dashboard."""

from pathlib import Path
import importlib.util

__all__ = ["render_learner_analytics"]

_module_path = Path(__file__).resolve().parent / "02_learner_analytics.py"
_spec = importlib.util.spec_from_file_location("app.pages.02_learner_analytics", _module_path)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)  # type: ignore

render_learner_analytics = _module.render_learner_analytics
