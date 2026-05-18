"""AI Insights page (deterministic signals + LLM scaffold)

This page surfaces simple, deterministic business signals and provides
placeholders for future LLM-assisted explanations and suggested actions.
"""
import streamlit as st
import pandas as pd

from app.services.insight_service import InsightService
from app.services import df_to_csv_bytes
from app.components import render_empty_state, render_section_title


def render_ai_insights():
    render_section_title(
        "🤖 AI Insights",
        "Deterministic business signals and anomaly detection. Placeholders for future LLM explanations.",
    )

    with st.spinner("Computing insights..."):
        out = InsightService.generate_insights(sample_n=25)

    summary: pd.DataFrame = out.get("summary")
    churn_anom: pd.DataFrame = out.get("churn_anomalies")
    drops: pd.DataFrame = out.get("engagement_drop_candidates")
    at_risk: pd.DataFrame = out.get("at_risk_segments")

    st.subheader("Summary Metrics")
    st.table(summary.set_index("metric")["value"])

    st.subheader("Top At-Risk Segments")
    if not at_risk.empty:
        st.dataframe(at_risk, use_container_width=True)
    else:
        st.info("No segment-level data available; ensure features include `segment` or `churn_risk`.")

    st.subheader("Churn Anomalies (sample)")
    if churn_anom is None or churn_anom.empty:
        render_empty_state("No churn anomalies detected with the current thresholds.")
    else:
        st.dataframe(churn_anom.head(50), use_container_width=True)
        b = df_to_csv_bytes(churn_anom)
        st.download_button("Download churn anomalies (CSV)", data=b, file_name="churn_anomalies.csv", mime="text/csv")

    st.subheader("Engagement Drop Candidates")
    if drops is None or drops.empty:
        render_empty_state("No engagement-drop candidates detected.")
    else:
        st.dataframe(drops.head(50), use_container_width=True)
        b2 = df_to_csv_bytes(drops)
        st.download_button("Download drop candidates (CSV)", data=b2, file_name="engagement_drop_candidates.csv", mime="text/csv")

    st.divider()
    st.subheader("LLM Insight Placeholder")
    st.info("LLM-based explanations and actions will appear here once integrated.")
