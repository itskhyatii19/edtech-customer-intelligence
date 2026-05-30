"""Predictive Analytics page showcasing churn models and explainability.

This page presents a business-ready churn risk dashboard, at-risk learner
table, anomaly panels, recommendations, and a concise executive summary.

Note: this view performs defensive validation and shows friendly empty
states when required features are missing.
"""

import streamlit as st
import pandas as pd
from typing import Dict

from app.components import (
    render_page_header,
    render_dashboard_card,
    render_insight_cards,
    render_empty_state,
    info_banner,
)
from app.services import DataLoader
from app.services import PredictiveService, AnomalyService, RecommendationService


REQUIRED_FEATURES = [
    "uuid",
    "engagement_score",
    "inactive_days",
    "activity_count",
    "churn_score",
]


def _ensure_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Provide defaults for missing columns so downstream UI doesn't break
    if "churn_probability" not in df.columns:
        df["churn_probability"] = PredictiveService.predict(df)
    if "churn_risk" not in df.columns and "churn_probability" in df.columns:
        df["churn_risk"] = pd.cut(df["churn_probability"], bins=[-1, 0.33, 0.66, 1.0], labels=["low", "medium", "high"]).astype(object)
    if "activity_per_day" not in df.columns:
        if "days_active" in df.columns and df["days_active"].notna().any():
            df["activity_per_day"] = df["activity_count"].fillna(0) / df["days_active"].replace(0, 1)
        else:
            df["activity_per_day"] = df["activity_count"].fillna(0)
    if "review_sentiment_score" not in df.columns:
        df["review_sentiment_score"] = df.get("review_sentiment_score", 0.0)
    if "review_length" not in df.columns:
        df["review_length"] = df.get("review_length", 0)
    return df


def _validate_presence(df: pd.DataFrame, required: list) -> Dict[str, bool]:
    missing = [c for c in required if c not in df.columns]
    return {"ok": len(missing) == 0, "missing": missing}


def render() -> None:
    render_page_header("Predictive Analytics", "Churn risk, anomalies, and recommended interventions.")

    with st.spinner("Loading features..."):
        df = DataLoader.load_features()

    if df is None or df.empty:
        render_empty_state("Feature data unavailable.", "Run feature engineering or check raw CSV sources.")
        return

    # Defensive validation
    val = _validate_presence(df, REQUIRED_FEATURES)
    if not val["ok"]:
        info_banner(f"Missing expected feature columns: {', '.join(val['missing'])}", variant="warning")

    df = _ensure_columns(df)

    # --- Model Status Section ---
    st.markdown("### Model Status")
    col1, col2, col3, col4 = st.columns(4, gap="large")
    
    model_status = PredictiveService.get_model_status()
    with col1:
        status_text = "Trained" if model_status["model_loaded"] else "Not Trained"
        st.metric("Status", status_text)
    with col2:
        st.metric("Model Type", model_status.get("model_type", "N/A"))
    with col3:
        auc = model_status.get("auc")
        st.metric("Validation AUC", f"{auc:.3f}" if auc else "N/A")
    with col4:
        st.metric("Sample Size", f"{model_status.get('sample_size', 0):,}")
    
    # Show training date
    if model_status.get("training_date"):
        st.caption(f"Last trained: {model_status['training_date']}")
    
    # Auto-train if not trained
    if not model_status["model_loaded"]:
        with st.expander("⚠️ No trained model. Click to train now.", expanded=False):
            if st.button("🚀 Train Churn Model"):
                with st.spinner("Training model on available data..."):
                    result = PredictiveService.train_and_save(df, model_type="random_forest")
                if result["success"]:
                    st.success(f"✅ Model trained and saved to `{result['model_path']}`")
                    st.json(result["metadata"])
                    st.rerun()
                else:
                    st.error(f"❌ Training failed: {result['error_msg']}")
    
    if model_status.get("fallback"):
        info_banner("Using deterministic fallback scoring (no ML model).", variant="info")
    
    st.divider()
    st.markdown("### Churn Risk Dashboard")
    counts = df["churn_risk"].value_counts().reindex(["high", "medium", "low"]).fillna(0).astype(int)
    # Cards
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        render_dashboard_card("High risk", f"{counts.get('high',0):,}", caption="Learners with high churn probability", badge="Risk")
    with col2:
        render_dashboard_card("Medium risk", f"{counts.get('medium',0):,}", caption="Learners with medium churn probability", badge="Risk")
    with col3:
        render_dashboard_card("Low risk", f"{counts.get('low',0):,}", caption="Learners with low churn probability", badge="Risk")

    # Distribution chart
    st.divider()
    st.markdown("#### Risk distribution")
    try:
        chart_data = df["churn_probability"].dropna()
        if chart_data.empty:
            st.info("No churn probability scores available to plot.")
        else:
            hist = pd.cut(chart_data, bins=10).value_counts().sort_index()
            st.bar_chart(hist)
    except Exception:
        st.info("Unable to render risk distribution chart.")

    # --- At-Risk Learner Table ---
    st.divider()
    st.markdown("### At-Risk Learners")
    display_cols = ["uuid", "churn_probability", "inactive_days", "engagement_score"]
    missing_display = [c for c in display_cols if c not in df.columns]
    if missing_display:
        render_empty_state("Required learner columns missing.", f"Missing: {', '.join(missing_display)}")
    else:
        table = df[display_cols].rename(columns={"uuid": "learner_id", "churn_probability": "risk_score", "inactive_days": "inactivity_days"}).copy()
        # Add recommended action
        recs = RecommendationService.recommend(df)
        if not recs.empty and "recommendation" in recs.columns:
            rec_map = recs.set_index("uuid")["recommendation"].to_dict()
            table["recommended_action"] = table["learner_id"].map(rec_map).fillna("Monitor")
        else:
            table["recommended_action"] = "Monitor"

        # Sort by risk_score desc
        table = table.sort_values(by="risk_score", ascending=False).reset_index(drop=True)
        st.dataframe(table.head(500), use_container_width=True)

    # --- Anomaly Detection Panel ---
    st.divider()
    st.markdown("### Anomalies & Alerts")
    with st.expander("Engagement anomalies (low engagement)", expanded=False):
        eng_anom = AnomalyService.detect_engagement_anomalies(df)
        if eng_anom is None or eng_anom.empty:
            st.info("No engagement anomalies detected.")
        else:
            st.dataframe(eng_anom[["uuid", "engagement_score", "anomaly_severity"]].head(200))

    with st.expander("Inactivity spikes", expanded=False):
        spike = AnomalyService.detect_inactivity_spikes(df)
        if spike is None or spike.empty:
            st.info("No inactivity spikes detected.")
        else:
            st.dataframe(spike[["uuid", "inactive_days", "severity"]].head(200))

    with st.expander("Review sentiment anomalies", expanded=False):
        # Lightweight sentiment anomaly: users with very negative sentiment score
        if "review_sentiment_score" not in df.columns:
            st.info("No review sentiment data available.")
        else:
            negs = df[df["review_sentiment_score"] <= -0.5]
            if negs.empty:
                st.info("No review sentiment anomalies detected.")
            else:
                st.dataframe(negs[["uuid", "review_sentiment_score", "review_length"]].head(200))

    # --- Recommendation Engine Output ---
    st.divider()
    st.markdown("### Recommendations & Actions")
    try:
        recs_all = RecommendationService.recommend(df)
        if recs_all is None or recs_all.empty:
            st.info("No recommendations available. Ensure churn probabilities are computed.")
        else:
            st.dataframe(recs_all.head(200), use_container_width=True)
    except Exception:
        st.info("Recommendation engine unavailable.")

    # --- Executive Summary ---
    st.divider()
    st.markdown("### Executive Summary")
    insights = []
    try:
        avg_eng = float(df.get("engagement_score", pd.Series([0])).mean())
        pct_high = float((df.get("churn_risk", pd.Series(dtype=object)) == "high").mean())
        top_issue = "High churn concentration in a specific segment" if pct_high > 0.05 else "No concentrated high-risk segment"
        insights.append({"title": "Retention Health", "detail": f"Average engagement {avg_eng:.2f}; {pct_high:.1%} high risk."})
        insights.append({"title": "Top Concern", "detail": top_issue})
        insights.append({"title": "Recommended Action", "detail": "Prioritize re-engagement campaigns for high-risk learners; review content for negative sentiment clusters."})
    except Exception:
        insights.append({"title": "No executive insights", "detail": "Insufficient data to compute summary."})

    render_insight_cards(insights, columns=3)
