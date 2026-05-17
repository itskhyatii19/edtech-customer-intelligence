"""Home dashboard page - Executive overview"""

import streamlit as st
import pandas as pd
from app.services import DataLoader, AnalyticsService
from app.components import (
    metric_row,
    engagement_histogram,
    inactivity_histogram,
    segment_pie_chart,
    churn_distribution_chart,
    top_reviewers_chart,
)


def render_home():
    """Render the home dashboard page"""

    st.title("📊 Platform Overview")
    st.write(
        "Real-time analytics dashboard for EdTech student engagement and success"
    )

    # ============================================================================
    # Section 1: Key Metrics
    # ============================================================================
    st.header("📈 Key Metrics")

    # Get all metrics
    engagement_metrics = AnalyticsService.get_engagement_metrics()
    retention_metrics = AnalyticsService.get_retention_metrics()
    churn_metrics = AnalyticsService.get_churn_metrics()
    review_stats = AnalyticsService.get_review_statistics()

    # Display KPI cards
    metric_row(
        [
            {
                "label": "Total Learners",
                "value": str(DataLoader.get_user_count()),
                "help": "Total number of registered users",
            },
            {
                "label": "Avg Engagement Score",
                "value": f"{engagement_metrics.get('avg_engagement', 0):.2%}",
                "help": "Average engagement score across all learners",
            },
            {
                "label": "Active Learners",
                "value": str(retention_metrics.get("active_users", 0)),
                "delta": f"{retention_metrics.get('active_percentage', 0):.1f}%",
                "help": "Users active in the last 30 days",
            },
            {
                "label": "At-Risk Learners",
                "value": str(churn_metrics.get("high_risk_count", 0)),
                "delta": f"{churn_metrics.get('high_risk_percentage', 0):.1f}%",
                "delta_color": "inverse",
                "help": "High churn risk based on engagement patterns",
            },
        ]
    )

    # ============================================================================
    # Section 2: Review Statistics
    # ============================================================================
    st.header("💬 Review Intelligence")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Reviews",
            review_stats.get("total_reviews", 0),
            help="Number of student reviews collected",
        )

    with col2:
        st.metric(
            "Unique Reviewers",
            review_stats.get("unique_reviewers", 0),
            help="Number of students who submitted reviews",
        )

    with col3:
        if "avg_rating" in review_stats:
            st.metric(
                "Avg Rating",
                f"{review_stats.get('avg_rating', 0):.2f}⭐",
                help="Average rating from all reviews",
            )
        else:
            st.metric("Avg Rating", "N/A")

    # ============================================================================
    # Section 3: Visualizations - Row 1
    # ============================================================================
    st.header("📊 Engagement Analysis")

    col1, col2 = st.columns(2)

    # Engagement distribution
    with col1:
        engagement_dist = AnalyticsService.get_engagement_distribution()
        if engagement_dist:
            fig = engagement_histogram(engagement_dist)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No engagement data available")

    # Inactivity distribution
    with col2:
        inactivity_dist = AnalyticsService.get_inactivity_distribution()
        if inactivity_dist:
            fig = inactivity_histogram(inactivity_dist)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No inactivity data available")

    # ============================================================================
    # Section 4: Visualizations - Row 2
    # ============================================================================
    col1, col2 = st.columns(2)

    # User segments
    with col1:
        segment_counts = DataLoader.get_segment_counts()
        if segment_counts:
            fig = segment_pie_chart(segment_counts)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No segment data available")

    # Churn risk distribution
    with col2:
        churn_dist = DataLoader.get_churn_distribution()
        if churn_dist:
            fig = churn_distribution_chart(churn_dist)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No churn data available")

    # ============================================================================
    # Section 5: Top Reviewers
    # ============================================================================
    st.header("⭐ Top Reviewers")

    top_reviewers = AnalyticsService.get_top_reviewers(n=10)
    if top_reviewers is not None and len(top_reviewers) > 0:
        col1, col2 = st.columns([2, 1])

        with col1:
            fig = top_reviewers_chart(top_reviewers)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.write("### Review Leaders")
            st.dataframe(top_reviewers, hide_index=True, use_container_width=True)
    else:
        st.info("No reviewer data available")

    # ============================================================================
    # Section 6: Segment Comparison Table
    # ============================================================================
    st.header("📋 Segment Comparison")

    segment_comparison = AnalyticsService.get_segment_comparison()
    if segment_comparison is not None:
        st.dataframe(segment_comparison, use_container_width=True)
    else:
        st.info("No segment comparison data available")

    # ============================================================================
    # Footer
    # ============================================================================
    st.divider()
    st.caption(
        "💡 **Tip:** Use the sidebar to navigate to detailed analytics pages. "
        "Data is automatically cached for 1 hour."
    )
