"""Learner Analytics page implementation."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from app.components import (
    churn_distribution_chart,
    engagement_histogram,
    engagement_inactivity_scatter,
    inactivity_histogram,
    retention_curve_chart,
    segment_pie_chart,
    activity_frequency_histogram,
    render_dashboard_card,
    render_empty_state,
    render_insight_cards,
    render_section_title,
)
from app.services import DataLoader
from app.services.export_service import df_to_csv_bytes


def _build_engagement_bins(df: pd.DataFrame) -> dict[str, int]:
    labels = ["0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1.0"]
    bins = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    distribution = pd.cut(df["engagement_score"], bins=bins, labels=labels, right=False)
    return distribution.value_counts().sort_index().to_dict()


def _build_inactivity_buckets(df: pd.DataFrame) -> dict[str, int]:
    labels = ["0-30d", "30-60d", "60-90d", "90-180d", "180-365d"]
    bins = [0, 30, 60, 90, 180, 365]
    distribution = pd.cut(df["inactive_days"], bins=bins, labels=labels, right=False)
    return distribution.value_counts().sort_index().to_dict()


def _build_retention_curve(df: pd.DataFrame) -> dict[str, float]:
    max_inactive = int(df["inactive_days"].max()) if not df["inactive_days"].empty else 365
    buckets = [0, 7, 14, 30, 60, 90, 180, max_inactive + 1]
    labels = ["0-7d", "7-14d", "14-30d", "30-60d", "60-90d", "90-180d", f"180-{max_inactive}d"]
    cuts = pd.cut(df["inactive_days"], bins=buckets, labels=labels, right=False, include_lowest=True)
    bucket_counts = cuts.value_counts().sort_index()
    total = len(df)
    return {label: float(bucket_counts.get(label, 0) / total * 100) for label in labels}


def _build_activity_frequency(df: pd.DataFrame) -> dict[str, int]:
    max_activity = int(df["activity_count"].max()) if not df["activity_count"].empty else 1
    bins = [0, 1, 3, 5, 10, 20, 50, 100, max_activity + 1]
    labels = ["0", "1", "2-3", "4-5", "6-10", "11-20", "21-50", "51-100", f"100+ ({max_activity})"]
    distribution = pd.cut(df["activity_count"], bins=bins, labels=labels, right=False)
    return distribution.value_counts().sort_index().to_dict()


def _build_segment_comparison(df: pd.DataFrame) -> pd.DataFrame:
    segment_stats = (
        df.groupby("user_segment")
        .agg(
            Users=("uuid", "count"),
            AvgEngagement=("engagement_score", "mean"),
            AvgActivity=("activity_count", "mean"),
            AvgInactiveDays=("inactive_days", "mean"),
        )
        .round(2)
        .reset_index()
    )
    return segment_stats


def _build_insights(df: pd.DataFrame) -> list[dict[str, str]]:
    total = len(df)
    if total == 0:
        return []

    segment_counts = df["user_segment"].value_counts(normalize=True)
    high_risk_pct = len(df[df["churn_risk"] == "high"]) / total * 100
    inactive_pct = len(df[df["inactive_days"] > 180]) / total * 100
    highly_active_pct = len(df[df["user_segment"] == "highly_active"]) / total * 100

    return [
        {
            "title": "Majority at moderate or low engagement",
            "detail": f"{(segment_counts.get('low_active', 0) + segment_counts.get('moderate', 0)) * 100:.1f}% of learners are in lower activity segments.",
        },
        {
            "title": "Long inactivity signals churn",
            "detail": f"{inactive_pct:.1f}% of learners have been inactive more than 180 days.",
        },
        {
            "title": "Highly active cohort remains small",
            "detail": f"Only {highly_active_pct:.1f}% of learners are classified as highly active.",
        },
        {
            "title": "High churn risk is material",
            "detail": f"{high_risk_pct:.1f}% of the cohort is currently in the high churn risk category.",
        },
    ]


def render() -> None:
    """Render the Learner Analytics dashboard page."""
    render_section_title(
        "Learner Analytics",
        "Explore cohort filters, churn risk, and retention trends in one compact view.",
    )

    with st.spinner("Loading learner cohort data..."):
        df = DataLoader.load_features()

    if df is None:
        render_empty_state(
            "Learner feature data is unavailable.",
            "Check the data sources and refresh cache settings.",
        )
        return

    with st.expander("Filters", expanded=False):
        engagement_range = st.slider(
            "Engagement range",
            min_value=0.0,
            max_value=1.0,
            value=(0.0, 1.0),
            step=0.05,
        )

        max_inactive = int(df["inactive_days"].max()) if "inactive_days" in df.columns else 365
        inactivity_range = st.slider(
            "Days inactive",
            min_value=0,
            max_value=max_inactive,
            value=(0, min(180, max_inactive)),
            step=5,
        )

        segment_options = sorted(df["user_segment"].dropna().unique().tolist())
        selected_segments = st.multiselect(
            "Segment",
            options=segment_options,
            default=segment_options,
        )

        churn_options = sorted(df["churn_risk"].dropna().unique().tolist())
        selected_churn = st.multiselect(
            "Churn risk",
            options=churn_options,
            default=churn_options,
        )

        if st.button("Reset filters"):
            st.experimental_rerun()

    filtered = df[
        (df["engagement_score"] >= engagement_range[0])
        & (df["engagement_score"] <= engagement_range[1])
        & (df["inactive_days"] >= inactivity_range[0])
        & (df["inactive_days"] <= inactivity_range[1])
        & (df["user_segment"].isin(selected_segments))
        & (df["churn_risk"].isin(selected_churn))
    ].copy()

    if filtered.empty:
        render_empty_state(
            "No learners match the selected filters.",
            "Broaden the cohort filters or reset them to see more data.",
        )
        return

    total_learners = len(filtered)
    active_learners = int((filtered["inactive_days"] <= 30).sum())
    inactive_learners = total_learners - active_learners
    avg_engagement = filtered["engagement_score"].mean()
    avg_inactive_days = filtered["inactive_days"].mean()
    high_risk_users = int((filtered["churn_risk"] == "high").sum())

    col1, col2, col3, col4 = st.columns(4, gap="large")
    with col1:
        render_dashboard_card(
            title="Filtered learners",
            value=f"{total_learners:,}",
            caption="Cohort matching current filters.",
            badge="Cohort",
        )
    with col2:
        render_dashboard_card(
            title="Active learners",
            value=f"{active_learners:,}",
            caption="Learners active in the last 30 days.",
            badge="Retention",
        )
    with col3:
        render_dashboard_card(
            title="Inactive learners",
            value=f"{inactive_learners:,}",
            caption="Learners inactive for longer than 30 days.",
            badge="Engagement",
        )
    with col4:
        render_dashboard_card(
            title="High churn risk",
            value=f"{high_risk_users:,}",
            caption="Learners flagged as high churn risk.",
            badge="Churn",
        )

    st.markdown("---")
    st.subheader("Retention and engagement")
    col1, col2 = st.columns([1.4, 1], gap="large")
    with col1:
        st.plotly_chart(engagement_histogram(_build_engagement_bins(filtered), title="Engagement distribution"), use_container_width=True)
        st.plotly_chart(retention_curve_chart(_build_retention_curve(filtered), title="Retention curve"), use_container_width=True)
    with col2:
        st.plotly_chart(inactivity_histogram(_build_inactivity_buckets(filtered), title="Inactive days distribution"), use_container_width=True)
        st.plotly_chart(activity_frequency_histogram(_build_activity_frequency(filtered), title="Activity frequency"), use_container_width=True)

    st.markdown("---")
    st.subheader("Segment and churn overview")
    segment_summary = _build_segment_comparison(filtered)
    segment_counts = filtered["user_segment"].value_counts().to_dict()
    churn_counts = filtered["churn_risk"].value_counts().to_dict()

    col1, col2 = st.columns(2, gap="large")
    with col1:
        if segment_counts:
            st.plotly_chart(segment_pie_chart(segment_counts, title="Segment mix"), use_container_width=True)
        else:
            render_empty_state("No segment data available.")
    with col2:
        if churn_counts:
            st.plotly_chart(churn_distribution_chart(churn_counts, title="Churn risk mix"), use_container_width=True)
        else:
            render_empty_state("No churn distribution data available.")

    st.markdown("---")
    st.subheader("Engagement vs inactivity")
    st.plotly_chart(engagement_inactivity_scatter(filtered, title="Engagement vs inactivity"), use_container_width=True)

    st.markdown("---")
    st.subheader("Segment comparison")
    st.dataframe(segment_summary, use_container_width=True)

    st.markdown("---")
    render_section_title("Insights")
    render_insight_cards(_build_insights(filtered), columns=2)

    st.download_button(
        "Download filtered cohort",
        data=df_to_csv_bytes(filtered),
        file_name="learner_analytics_cohort.csv",
        mime="text/csv",
    )
    st.caption("Filtered learner analytics are refreshed as filters change.")
