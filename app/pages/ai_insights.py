"""AI Insights page (deterministic signals + LLM scaffold)."""

import streamlit as st
import pandas as pd

from app.services.insight_service import InsightService
from app.services import df_to_csv_bytes
from app.services import DataLoader
from app.components import (
    render_dashboard_card,
    render_empty_state,
    render_insight_cards,
    render_section_title,
)


def render() -> None:
    render_section_title(
        "AI Insights",
        "Deterministic signals, churn warnings, and action-oriented recommendations.",
    )

    with st.spinner("Computing insights..."):
        out = InsightService.generate_insights(sample_n=25)

    summary: pd.DataFrame = out.get("summary") or pd.DataFrame()
    churn_anom: pd.DataFrame = out.get("churn_anomalies") or pd.DataFrame()
    drops: pd.DataFrame = out.get("engagement_drop_candidates") or pd.DataFrame()
    at_risk: pd.DataFrame = out.get("at_risk_segments") or pd.DataFrame()

    high_risk_pct = 0.0
    total_users = 0
    avg_engagement = 0.0
    if not summary.empty:
        if "high_risk_pct" in summary["metric"].values:
            high_risk_pct = float(summary.loc[summary["metric"] == "high_risk_pct", "value"].squeeze() or 0.0)
        if "total_users" in summary["metric"].values:
            total_users = int(summary.loc[summary["metric"] == "total_users", "value"].squeeze() or 0)
        if "avg_engagement" in summary["metric"].values:
            avg_engagement = float(summary.loc[summary["metric"] == "avg_engagement", "value"].squeeze() or 0.0)

    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        render_dashboard_card(
            title="Total learners",
            value=f"{total_users:,}",
            caption="Learner cohort size used for insights.",
            badge="Scope",
        )
    with col2:
        render_dashboard_card(
            title="Avg engagement",
            value=f"{avg_engagement:.0%}",
            caption="Average engagement across the cohort.",
            badge="Engagement",
        )
    with col3:
        render_dashboard_card(
            title="High churn risk",
            value=f"{high_risk_pct:.1f}%",
            caption="Learners with elevated churn risk.",
            badge="Retention",
        )

    st.markdown("---")
    st.subheader("Signal summary")
    risk_insights = []
    if total_users > 0:
        risk_insights = [
            {
                "title": "Churn risk is concentrated",
                "detail": f"{high_risk_pct:.1f}% of learners are currently flagged as high churn risk, indicating a key retention opportunity.",
            },
            {
                "title": "Engagement baseline",
                "detail": f"Average engagement is {avg_engagement:.0%}, suggesting room to improve overall learner activation.",
            },
            {
                "title": "Decision focus",
                "detail": "Prioritize campaigns for learners with low engagement and high inactivity to reduce churn.",
            },
        ]
    else:
        risk_insights = [
            {
                "title": "No insights available",
                "detail": "Load feature data to generate churn and engagement signals.",
            }
        ]
    render_insight_cards(risk_insights, columns=3)

    st.markdown("---")
    st.subheader("Top at-risk segments")
    if not at_risk.empty:
        st.dataframe(at_risk, use_container_width=True)
    else:
        render_empty_state("No at-risk segments detected. Ensure churn segmentation is computed.")

    st.markdown("---")
    st.subheader("Churn anomalies")
    if not churn_anom.empty:
        st.write(f"Showing {len(churn_anom)} churn anomaly candidates.")
        st.dataframe(churn_anom.head(40), use_container_width=True)
        st.download_button(
            "Download churn anomalies (CSV)",
            data=df_to_csv_bytes(churn_anom),
            file_name="churn_anomalies.csv",
            mime="text/csv",
        )
    else:
        render_empty_state("No churn anomalies detected with the current thresholds.")

    st.markdown("---")
    st.subheader("Engagement drop candidates")
    if not drops.empty:
        st.write(f"Showing {len(drops)} low-engagement candidates.")
        st.dataframe(drops.head(40), use_container_width=True)
        st.download_button(
            "Download drop candidates (CSV)",
            data=df_to_csv_bytes(drops),
            file_name="engagement_drop_candidates.csv",
            mime="text/csv",
        )
    else:
        render_empty_state("No low-engagement candidates were identified.")

    st.markdown("---")
    st.subheader("Actionable recommendations")
    st.write(
        "- Focus retention outreach on learners with high churn risk and low engagement.\n"
        "- Use review feedback sentiment to guide course quality improvements.\n"
        "- Monitor segment performance monthly and update engagement campaigns accordingly."
    )
