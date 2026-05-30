"""Predictive modeling service: training, inference, and explainability.

This module is intentionally defensive: heavy ML imports are optional and
are only required when training/prediction features are used. If packages
like `sklearn`, `xgboost`, or `shap` are not available the service falls
back to deterministic scoring so the app remains runnable.
"""
from __future__ import annotations

import json
import logging
import os
import pickle
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

import pandas as pd

try:
    from sklearn.ensemble import RandomForestClassifier, IsolationForest
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.compose import ColumnTransformer
    from sklearn.metrics import roc_auc_score
    SKLEARN_AVAILABLE = True
except Exception:
    SKLEARN_AVAILABLE = False

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except Exception:
    XGBOOST_AVAILABLE = False

try:
    import shap
    SHAP_AVAILABLE = True
except Exception:
    SHAP_AVAILABLE = False

from app.services.logger import get_logger

logger = get_logger(__name__)


class PredictiveService:
    """Service to train and serve churn prediction models."""

    MODEL_REGISTRY: Dict[str, Any] = {}

    @staticmethod
    def _feature_columns() -> List[str]:
        # Return features that exist in the data; missing ones will be computed
        return [
            "engagement_score",
            "inactive_days",
            "activity_count",
            "user_segment",
        ]

    @staticmethod
    def train(df: pd.DataFrame, model_type: str = "random_forest", test_size: float = 0.2, random_state: int = 42) -> Dict[str, Any]:
        if df is None or df.empty:
            raise ValueError("Training data is empty")

        features = PredictiveService._feature_columns()
        # Filter to only available columns
        available_features = [f for f in features if f in df.columns]
        
        if not available_features:
            raise ValueError("No feature columns available in training data")

        X = df[available_features].copy()
        y = (df.get("churn_risk", "low") == "high").astype(int)

        # Simple preprocessing: numeric vs categorical
        numeric_cols = [c for c in X.columns if c not in ("user_segment",)]
        categorical_cols = ["user_segment"] if "user_segment" in X.columns else []

        if SKLEARN_AVAILABLE:
            preprocessor = ColumnTransformer(
                transformers=[
                    ("num", StandardScaler(), numeric_cols),
                    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
                ]
            )

            if model_type == "xgboost" and XGBOOST_AVAILABLE:
                model = xgb.XGBClassifier(random_state=random_state, use_label_encoder=False, eval_metric="logloss")
            elif model_type == "logistic":
                model = LogisticRegression(max_iter=500, random_state=random_state)
            else:
                model = RandomForestClassifier(n_estimators=200, random_state=random_state)

            pipeline = Pipeline([("pre", preprocessor), ("clf", model)])

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
            pipeline.fit(X_train, y_train)

            y_prob = pipeline.predict_proba(X_test)[:, 1] if hasattr(pipeline, "predict_proba") else pipeline.predict(X_test)
            auc = float(roc_auc_score(y_test, y_prob)) if len(set(y_test)) > 1 else 0.0

            PredictiveService.MODEL_REGISTRY["pipeline"] = pipeline
            PredictiveService.MODEL_REGISTRY["auc"] = auc
            PredictiveService.MODEL_REGISTRY["feature_cols"] = available_features

            logger.info("Trained predictive model type=%s auc=%.4f features=%s", model_type, auc, available_features)
            return {"pipeline": pipeline, "auc": auc}

        # Fallback deterministic model
        logger.warning("SKLearn not available; using deterministic fallback model.")
        score = PredictiveService._deterministic_score(df)
        PredictiveService.MODEL_REGISTRY["pipeline"] = None
        PredictiveService.MODEL_REGISTRY["auc"] = None
        PredictiveService.MODEL_REGISTRY["feature_cols"] = available_features
        return {"pipeline": None, "auc": None, "fallback_score": score}

    @staticmethod
    def predict(df: pd.DataFrame) -> pd.Series:
        if df is None or df.empty:
            return pd.Series(dtype=float)

        pipeline = PredictiveService.MODEL_REGISTRY.get("pipeline")
        feature_cols = PredictiveService.MODEL_REGISTRY.get("feature_cols", PredictiveService._feature_columns())
        
        # Filter to available features
        available_cols = [c for c in feature_cols if c in df.columns]
        
        if not pipeline or not available_cols:
            return PredictiveService._deterministic_score(df)

        try:
            X = df[available_cols].copy()
            if hasattr(pipeline, "predict_proba"):
                probs = pipeline.predict_proba(X)[:, 1]
            else:
                probs = pipeline.predict(X)
            return pd.Series(probs, index=df.index)
        except Exception as e:
            logger.warning("Prediction failed: %s; using fallback", e)
            return PredictiveService._deterministic_score(df)

    @staticmethod
    def feature_importance(top_n: int = 10) -> pd.DataFrame:
        pipeline = PredictiveService.MODEL_REGISTRY.get("pipeline")
        if pipeline is None:
            return pd.DataFrame()

        clf = pipeline.named_steps.get("clf")
        if hasattr(clf, "feature_importances_"):
            imp = clf.feature_importances_
            # Attempt to get feature names from preprocessor
            try:
                pre = pipeline.named_steps.get("pre")
                num_cols = pre.transformers_[0][2]
                cat_enc = pre.transformers_[1][1]
                cat_cols = []
                if hasattr(cat_enc, "get_feature_names_out"):
                    cat_cols = list(cat_enc.get_feature_names_out())
                features = list(num_cols) + cat_cols
            except Exception:
                features = [f"f{i}" for i in range(len(imp))]

            df = pd.DataFrame({"feature": features, "importance": imp}).sort_values("importance", ascending=False).head(top_n)
            return df

        return pd.DataFrame()

    @staticmethod
    def _deterministic_score(df: pd.DataFrame) -> pd.Series:
        # Simple deterministic risk score combining engagement and inactivity
        eng = df.get("engagement_score")
        if eng is None or (isinstance(eng, int)):
            eng = pd.Series(0, index=df.index)
        elif not isinstance(eng, pd.Series):
            eng = pd.Series(eng, index=df.index)
        eng = eng.fillna(0).clip(0, 1)
        
        inactive = df.get("inactive_days")
        if inactive is None or isinstance(inactive, int):
            inactive = pd.Series(0, index=df.index)
        elif not isinstance(inactive, pd.Series):
            inactive = pd.Series(inactive, index=df.index)
        inactive = inactive.fillna(0)
        
        activity_count = df.get("activity_count")
        if activity_count is None or isinstance(activity_count, int):
            activity_count = pd.Series(0, index=df.index)
        elif not isinstance(activity_count, pd.Series):
            activity_count = pd.Series(activity_count, index=df.index)
        activity_count = activity_count.fillna(0)
        
        # Simple scoring: high engagement and activity = low risk
        score = (1 - eng) * 0.5 + (inactive / 365.0) * 0.3 + (1 - (activity_count / (activity_count.max() + 1e-9))) * 0.2
        score = (score - score.min()) / (score.max() - score.min() + 1e-9)
        return pd.Series(score, index=df.index)

    @staticmethod
    def explain_instance(df: pd.DataFrame, idx) -> Dict[str, Any]:
        # Return simple contributor list; if SHAP available, compute SHAP values
        if SHAP_AVAILABLE and PredictiveService.MODEL_REGISTRY.get("pipeline") is not None:
            try:
                explainer = shap.Explainer(PredictiveService.MODEL_REGISTRY["pipeline"].named_steps["clf"])
                X = df[PredictiveService._feature_columns()].iloc[[idx]]
                vals = explainer(X)
                contributions = list(zip(PredictiveService._feature_columns(), vals.values[0]))
                return {"contributors": contributions}
            except Exception:
                pass

        # Fallback: show top features by heuristic
        row = df.loc[idx, PredictiveService._feature_columns()].to_dict()
        sorted_feats = sorted(row.items(), key=lambda x: abs(float(x[1]) if x[1] is not None else 0), reverse=True)
        return {"contributors": sorted_feats[:5]}

    @staticmethod
    def _get_model_dir() -> Path:
        model_dir = Path(__file__).parent.parent.parent / "models"
        model_dir.mkdir(exist_ok=True)
        return model_dir

    @staticmethod
    def train_and_save(df: pd.DataFrame, model_type: str = "random_forest") -> Dict[str, Any]:
        """Train model and persist to disk with metadata.
        
        Returns:
            dict with keys: success, model_path, metadata_path, metadata, error_msg
        """
        try:
            model_dir = PredictiveService._get_model_dir()
            
            # Train
            result = PredictiveService.train(df, model_type=model_type)
            
            # Build metadata
            metadata = {
                "timestamp": datetime.now().isoformat(),
                "model_type": model_type,
                "feature_count": len(PredictiveService._feature_columns()),
                "sample_size": len(df),
                "auc": result.get("auc"),
                "sklearn_available": SKLEARN_AVAILABLE,
                "xgboost_available": XGBOOST_AVAILABLE,
                "fallback": result.get("pipeline") is None,
            }
            
            # Save metadata
            metadata_path = model_dir / "metadata.json"
            with open(metadata_path, "w") as f:
                json.dump(metadata, f, indent=2)
            
            # Save model (if sklearn available)
            model_path = None
            if result.get("pipeline") is not None:
                model_path = model_dir / f"churn_model_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
                with open(model_path, "wb") as f:
                    pickle.dump(result["pipeline"], f)
                logger.info("Model saved to %s", model_path)
            
            logger.info("Training metadata saved to %s", metadata_path)
            return {
                "success": True,
                "model_path": str(model_path) if model_path else None,
                "metadata_path": str(metadata_path),
                "metadata": metadata,
                "error_msg": None,
            }
        
        except Exception as e:
            logger.error("Failed to train and save model: %s", str(e))
            return {
                "success": False,
                "model_path": None,
                "metadata_path": None,
                "metadata": None,
                "error_msg": str(e),
            }

    @staticmethod
    def load_model() -> Dict[str, Any]:
        """Load trained model from disk and restore MODEL_REGISTRY.
        
        Returns:
            dict with keys: success, model_loaded, metadata, error_msg
        """
        try:
            model_dir = PredictiveService._get_model_dir()
            metadata_path = model_dir / "metadata.json"
            
            if not metadata_path.exists():
                logger.warning("No model metadata found at %s", metadata_path)
                return {
                    "success": False,
                    "model_loaded": False,
                    "metadata": None,
                    "error_msg": "No trained model found",
                }
            
            # Load metadata
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
            
            # Attempt to load model file
            model_files = sorted(model_dir.glob("churn_model_*.pkl"), reverse=True)
            if model_files:
                with open(model_files[0], "rb") as f:
                    pipeline = pickle.load(f)
                    PredictiveService.MODEL_REGISTRY["pipeline"] = pipeline
                    PredictiveService.MODEL_REGISTRY["auc"] = metadata.get("auc")
                    logger.info("Model loaded from %s", model_files[0])
                    return {
                        "success": True,
                        "model_loaded": True,
                        "metadata": metadata,
                        "error_msg": None,
                    }
            else:
                logger.warning("No model pickle files found in %s", model_dir)
                return {
                    "success": True,
                    "model_loaded": False,
                    "metadata": metadata,
                    "error_msg": "Model metadata exists but no model file found",
                }
        
        except Exception as e:
            logger.error("Failed to load model: %s", str(e))
            return {
                "success": False,
                "model_loaded": False,
                "metadata": None,
                "error_msg": str(e),
            }

    @staticmethod
    def get_model_status() -> Dict[str, Any]:
        """Return current model status: loaded, metadata, auc, etc.
        
        Returns:
            dict with keys: model_loaded, model_type, training_date, sample_size, auc, fallback
        """
        model_dir = PredictiveService._get_model_dir()
        metadata_path = model_dir / "metadata.json"
        
        if not metadata_path.exists():
            return {
                "model_loaded": False,
                "model_type": None,
                "training_date": None,
                "sample_size": None,
                "auc": None,
                "fallback": True,
            }
        
        try:
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
            
            pipeline_loaded = PredictiveService.MODEL_REGISTRY.get("pipeline") is not None
            return {
                "model_loaded": pipeline_loaded,
                "model_type": metadata.get("model_type"),
                "training_date": metadata.get("timestamp"),
                "sample_size": metadata.get("sample_size"),
                "auc": metadata.get("auc"),
                "fallback": metadata.get("fallback", False),
            }
        except Exception:
            return {
                "model_loaded": False,
                "model_type": None,
                "training_date": None,
                "sample_size": None,
                "auc": None,
                "fallback": True,
            }

