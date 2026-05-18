"""Professional learner analytics dashboard page."""

from __future__ import annotations

from typing import Dict, List

import pandas as pd
import streamlit as st

from app.components import (
    churn_distribution_chart,
    engagement_histogram,
    engagement_inactivity_scatter,
    inactivity_histogram,
    metric_row,
    retention_curve_chart,
    segment_pie_chart,
    activity_frequency_histogram,
    render_empty_state,
    render_insight_cards,
    render_section_title,
)
from app.services import DataLoader
from app.services.export_service import df_to_csv_bytes


def _build_engagement_bins(df: pd.DataFrame) -> Dict[str, int]:
    labels = ["0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1.0"]
    bins = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    distribution = pd.cut(df["engagement_score"], bins=bins, labels=labels, right=False)
    return distribution.value_counts().sort_index().to_dict()


def _build_inactivity_buckets(df: pd.DataFrame) -> Dict[str, int]:
    labels = ["0-30d", "30-60d", "60-90d", "90-180d", "180-365d"]
    bins = [0, 30, 60, 90, 180, 365]
    distribution = pd.cut(df["inactive_days"], bins=bins, labels=labels, right=False)
    return distribution.value_counts().sort_index().to_dict()


def _build_retention_curve(df: pd.DataFrame) -> Dict[str, float]:
    max_inactive = int(df["inactive_days"].max()) if not df["inactive_days"].empty else 365
    buckets = [0, 7, 14, 30, 60, 90, 180, max_inactive + 1]
    labels = ["0-7d", "7-14d", "14-30d", "30-60d", "60-90d", "90-180d", f"180-{max_inactive}d"]
    cuts = pd.cut(df["inactive_days"], bins=buckets, labels=labels, right=False, include_lowest=True)
    bucket_counts = cuts.value_counts().sort_index()
    total = len(df)
    return {label: float(bucket_counts.get(label, 0) / total * 100) for label in labels}


def _build_activity_frequency(df: pd.DataFrame) -> Dict[str, int]:
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


def _build_insights(df: pd.DataFrame) -> List[Dict[str, str]]:
    total = len(df)
    if total == 0:
        return []

    segment_counts = df["user_segment"].value_counts(normalize=True)
    high_risk_pct = len(df[df["churn_risk"] == "high"]) / total * 100
    inactive_pct = len(df[df["inactive_days"] > 180]) / total * 100
    highly_active_pct = len(df[df["user_segment"] == "highly_active"]) / total * 100

    insights = [
        {
            "title": "Most users are in a low engagement segment",
            "detail": "Over {:.1f}% of filtered learners are in low activity or low engagement segments.".format(
                float(segment_counts.get("low_active", 0) + segment_counts.get("moderate", 0)) * 100
            ),
        },
        {
            "title": "Long inactivity is linked to churn risk",
            "detail": "{:.1f}% of filtered learners have been inactive more than 180 days, a sign of elevated churn risk.".format(
                inactive_pct
            ),
        },
        {
            "title": "Top cohort is highly active learners",
            "detail": "Highly active learners represent {:.1f}% of the filtered cohort and drive the strongest engagement.".format(
                highly_active_pct
            ),
        },
        {
            "title": "High churn risk segment requires attention",
            "detail": "{:.1f}% of filtered users are in the high churn risk category. Consider engagement recovery campaigns.".format(
                high_risk_pct
            ),
        },
    ]
    return insights


def _format_change(value: float, suffix: str = "%") -> str:
    return f"{value:.1f}{suffix}"


def render_learner_analytics() -> None:
    """Render the Learner Analytics dashboard page."""
    render_section_title(
        "👥 Learner Analytics",
        "Understand learner behavior with segment analysis, churn risk, retention curves, and product-ready insight cards.",
    )

    with st.spinner("Loading learner data..."):
        df = DataLoader.load_features()

    if df is None:
        render_empty_state(
            "Learner feature data is unavailable.",
            "Check the data source and cache settings before continuing.",
        )
        return

    side = st.sidebar
    side.header("Learner Analytics Filters")

    engagement_range = side.slider(
        "Engagement range",
        min_value=0.0,
        max_value=1.0,
        value=(0.0, 1.0),
        step=0.05,
    )

    max_inactive = int(df["inactive_days"].max()) if "inactive_days" in df.columns else 365
    inactivity_range = side.slider(
        "Inactivity days",
        min_value=0,
        max_value=max_inactive,
        value=(0, min(180, max_inactive)),
        step=5,
    )

    segment_options = sorted(df["user_segment"].dropna().unique().tolist())
    selected_segments = side.multiselect(
        "User segment",
        options=segment_options,
        default=segment_options,
    )

    churn_options = sorted(df["churn_risk"].dropna().unique().tolist())
    selected_churn = side.multiselect(
        "Churn risk",
        options=churn_options,
        default=churn_options,
    )

    side.markdown("---")
    if side.button("Reset filters"):
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
            "No learners match the selected filter criteria.",
            "Try broadening the filter selections or resetting the filters.",
        )
        return

    total_learners = len(filtered)
    active_learners = int((filtered["inactive_days"] <= 30).sum())
    inactive_learners = total_learners - active_learners
    avg_engagement = filtered["engagement_score"].mean()
    avg_inactive_days = filtered["inactive_days"].mean()
    high_risk_users = int((filtered["churn_risk"] == "high").sum())

    kpis = [
        {
            "label": "Total Learners",
            "value": f"{total_learners:,}",
            "delta": None,
            "help": "Total number of learners in the filtered cohort.",
        },
        {
            "label": "Active Learners",
            "value": f"{active_learners:,}",
            "delta": None,
            "help": "Learners with activity in the last 30 days.",
        },
        {
            "label": "Inactive Learners",
            "value": f"{inactive_learners:,}",
            "delta": None,
            "help": "Learners not active for more than 30 days.",
        },
    ]

    kpis2 = [
        {
            "label": "Avg Engagement",
            "value": f"{avg_engagement:.2%}",
            "help": "Average normalized engagement score for the filtered cohort.",
        },
        {
            "label": "Avg Inactivity",
            "value": f"{avg_inactive_days:.1f} days",
            "help": "Average number of days since the last learner activity.",
        },
        {
            "label": "High-Risk Churn",
            "value": f"{high_risk_users:,}",
            "help": "Filtered learners currently flagged as high churn risk.",
        },
    ]

    metric_row(kpis)
    metric_row(kpis2)

    render_section_title("Retention & Engagement Analytics")

    retention_data = _build_retention_curve(filtered)
    engagement_data = _build_engagement_bins(filtered)
    inactivity_data = _build_inactivity_buckets(filtered)
    activity_data = _build_activity_frequency(filtered)

    row1_col1, row1_col2 = st.columns([2, 1])
    with row1_col1:
        st.plotly_chart(engagement_histogram(engagement_data), use_container_width=True)
        st.plotly_chart(retention_curve_chart(retention_data), use_container_width=True)
    with row1_col2:
        st.plotly_chart(inactivity_histogram(inactivity_data), use_container_width=True)
        st.plotly_chart(activity_frequency_histogram(activity_data), use_container_width=True)

    render_section_title("Segment & Churn Risk Analysis")

    segment_summary = _build_segment_comparison(filtered)
    segment_counts = filtered["user_segment"].value_counts().to_dict()
    churn_counts = filtered["churn_risk"].value_counts().to_dict()

    seg_col1, seg_col2 = st.columns(2)
    with seg_col1:
        st.plotly_chart(segment_pie_chart(segment_counts), use_container_width=True)
    with seg_col2:
        st.plotly_chart(churn_distribution_chart(churn_counts), use_container_width=True)

    render_section_title("Segment comparison")
    st.dataframe(segment_summary, use_container_width=True)

    render_section_title("Engagement vs Inactivity")
    st.plotly_chart(engagement_inactivity_scatter(filtered), use_container_width=True)

    render_section_title("Product Insights")
    insights = _build_insights(filtered)
    if insights:
        render_insight_cards(insights, columns=2)
    else:
        render_empty_state("No insights available for this cohort.")

    st.download_button(
        "Download filtered learner cohort",
        data=df_to_csv_bytes(filtered),
        file_name="learner_analytics_cohort.csv",
        mime="text/csv",
    )
    st.caption(
        "Filtered charts are generated from learner feature data and updated immediately when filter values change."
    )
