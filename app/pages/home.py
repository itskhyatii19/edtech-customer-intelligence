"""Home dashboard page - Executive overview."""

import streamlit as st
from app.services import DataLoader, AnalyticsService
from app.services.insight_service import InsightService
from app.services.review_service import ReviewService
from app.components import (
    engagement_histogram,
    inactivity_histogram,
    segment_pie_chart,
    churn_distribution_chart,
    rating_histogram,
    sentiment_bar_chart,
    render_dashboard_card,
    render_empty_state,
    render_insight_cards,
    render_navigation_card,
    render_section_title,
)


def render() -> None:
    """Render the home dashboard page."""
    render_section_title(
        "Platform Overview",
        "A compact executive dashboard for learner engagement, churn risk, and review intelligence.",
    )

    engagement_metrics = AnalyticsService.get_engagement_metrics()
    retention_metrics = AnalyticsService.get_retention_metrics()
    churn_metrics = AnalyticsService.get_churn_metrics()
    review_stats = AnalyticsService.get_review_statistics()
    quick_insights = InsightService.generate_insights(sample_n=5)

    total_learners = DataLoader.get_user_count()
    high_risk_pct = churn_metrics.get("high_risk_percentage", 0.0)
    avg_engagement = engagement_metrics.get("avg_engagement", 0.0)
    total_reviews = review_stats.get("total_reviews", 0)
    avg_rating = review_stats.get("avg_rating")

    col1, col2, col3, col4 = st.columns(4, gap="large")
    with col1:
        render_dashboard_card(
            title="Total learners",
            value=f"{total_learners:,}",
            caption="Active users in the current cohort.",
            badge="Engagement",
        )
    with col2:
        render_dashboard_card(
            title="Avg engagement",
            value=f"{avg_engagement:.0%}",
            caption="Average engagement score across users.",
            badge="Engagement",
        )
    with col3:
        render_dashboard_card(
            title="High churn risk",
            value=f"{high_risk_pct:.1f}%",
            caption="Share of users classified as high risk.",
            badge="Churn",
            delta=f"{churn_metrics.get('high_risk_count', 0):,} learners",
        )
    with col4:
        render_dashboard_card(
            title="Review volume",
            value=f"{total_reviews:,}",
            caption="Review records available for analysis.",
            badge="Reviews",
        )

    st.markdown("---")
    st.subheader("Health snapshot")

    col1, col2 = st.columns([1.5, 1], gap="large")
    with col1:
        engagement_dist = AnalyticsService.get_engagement_distribution()
        if engagement_dist:
            st.plotly_chart(engagement_histogram(engagement_dist, title="Engagement distribution"), use_container_width=True)
        else:
            render_empty_state("No engagement data available.")

        segment_counts = DataLoader.get_segment_counts()
        if segment_counts:
            st.plotly_chart(segment_pie_chart(segment_counts, title="Engagement segments"), use_container_width=True)
        else:
            render_empty_state("Segment breakdown is unavailable.")

    with col2:
        inactivity_dist = AnalyticsService.get_inactivity_distribution()
        if inactivity_dist:
            st.plotly_chart(inactivity_histogram(inactivity_dist, title="Inactivity distribution"), use_container_width=True)
        else:
            render_empty_state("No inactivity data available.")

        churn_dist = DataLoader.get_churn_distribution()
        if churn_dist:
            st.plotly_chart(churn_distribution_chart(churn_dist, title="Churn distribution"), use_container_width=True)
        else:
            render_empty_state("Churn risk distribution is unavailable.")

    st.markdown("---")
    st.subheader("Review intelligence preview")
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        if avg_rating is not None:
            render_dashboard_card(
                title="Average rating",
                value=f"{avg_rating:.2f} ⭐",
                caption="Review sentiment averaged across all feedback.",
                badge="Reviews",
            )
        else:
            render_empty_state("Average rating is unavailable.")

        rating_dist = ReviewService.get_rating_distribution()
        if rating_dist:
            st.plotly_chart(rating_histogram(rating_dist, title="Rating distribution"), use_container_width=True)
        else:
            render_empty_state("Rating distribution is unavailable.")

    with col2:
        sentiment_dist = ReviewService.get_sentiment_distribution()
        if sentiment_dist:
            st.plotly_chart(sentiment_bar_chart(sentiment_dist, title="Sentiment mix"), use_container_width=True)
        else:
            render_empty_state("Sentiment distribution is unavailable.")

    st.markdown("---")
    st.subheader("AI-driven recommendations")
    insights = []
    if quick_insights and quick_insights.get("summary") is not None:
        summary = quick_insights["summary"]
        total_users = int(summary.loc[summary["metric"] == "total_users", "value"].squeeze() or 0)
        avg_engagement = float(summary.loc[summary["metric"] == "avg_engagement", "value"].squeeze() or 0.0)
        high_risk_pct = float(summary.loc[summary["metric"] == "high_risk_pct", "value"].squeeze() or 0.0)

        insights.append(
            {
                "title": "Engagement concentration",
                "detail": f"Average engagement is {avg_engagement:.0%} across {total_users:,} learners.",
            }
        )
        insights.append(
            {
                "title": "Churn risk hotspots",
                "detail": f"{high_risk_pct:.1f}% of users are flagged as high churn risk.",
            }
        )
        insights.append(
            {
                "title": "Review signal",
                "detail": f"Review volume is {total_reviews:,}; focus on negative sentiment themes.",
            }
        )
    else:
        insights.append(
            {
                "title": "Pending insight generation",
                "detail": "Run the feature pipeline to surface deterministic AI signals.",
            }
        )
    render_insight_cards(insights, columns=3)

    st.markdown("---")
    st.subheader("Quick navigation")
    quick_cols = st.columns(4, gap="large")
    with quick_cols[0]:
        render_navigation_card(
            title="Learner Analytics",
            description="Explore cohort segmentation, churn, and retention trends.",
            page_name="Learner Analytics",
            key="nav_learner",
        )
    with quick_cols[1]:
        render_navigation_card(
            title="AI Insights",
            description="Review anomaly, churn, and engagement signals.",
            page_name="AI Insights",
            key="nav_ai",
        )
    with quick_cols[2]:
        render_navigation_card(
            title="Review Intelligence",
            description="Analyze sentiment, themes, and top feedback.",
            page_name="Review Intelligence",
            key="nav_review",
        )
    with quick_cols[3]:
        render_navigation_card(
            title="Settings",
            description="Refresh cache and tune analysis parameters.",
            page_name="Settings",
            key="nav_settings",
        )

    st.caption("Balanced layout, compact cards, and actionable insights for a modern product-grade dashboard.")
