"""Review Intelligence page for student feedback analysis."""

import streamlit as st
from app.services.review_service import ReviewService
from app.components import (
    metric_row,
    rating_histogram,
    sentiment_bar_chart,
    keyword_bar_chart,
)
from app.services.export_service import get_filtered_reviews_csv


def render_review_intelligence():
    """Render the review intelligence dashboard page."""
    st.title("💬 Review Intelligence")
    st.write(
        "Analyze student feedback, sentiment, and common themes from course reviews."
    )

    reviews = ReviewService.load_reviews()
    if reviews is None:
        st.error("Unable to load review data. Check the data source and retry.")
        return

    # Compute key review metrics
    stats = ReviewService.get_review_statistics()
    avg_rating = stats.get("avg_rating")
    median_rating = stats.get("median_rating")

    metric_row(
        [
            {
                "label": "Total Reviews",
                "value": str(stats.get("total_reviews", 0)),
                "help": "Total review entries available for analysis.",
            },
            {
                "label": "Average Rating",
                "value": f"{avg_rating:.2f}" if avg_rating is not None else "N/A",
                "help": "Average score reported by reviewers.",
            },
            {
                "label": "Positive Reviews",
                "value": str(stats.get("positive_reviews", 0)),
                "delta": "+",
                "help": "Reviews with positive sentiment.",
            },
            {
                "label": "Negative Reviews",
                "value": str(stats.get("negative_reviews", 0)),
                "delta": "-",
                "delta_color": "inverse",
                "help": "Reviews with negative sentiment.",
            },
        ]
    )

    st.divider()

    # Review distribution charts
    st.subheader("Review Sentiment & Rating Distribution")
    col1, col2 = st.columns(2)

    with col1:
        rating_dist = ReviewService.get_rating_distribution()
        if rating_dist:
            fig = rating_histogram(rating_dist)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No rating distribution data available.")

    with col2:
        sentiment_dist = ReviewService.get_sentiment_distribution()
        if sentiment_dist:
            fig = sentiment_bar_chart(sentiment_dist)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No sentiment distribution data available.")

    st.divider()

    # Theme extraction
    st.subheader("Review Theme Extraction")
    st.write(
        "Discover the most common review keywords and themes across student feedback."
    )
    top_keywords = ReviewService.get_top_keywords(n=12)
    if top_keywords is not None and not top_keywords.empty:
        fig = keyword_bar_chart(top_keywords)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No keyword data available to display.")

    # Show themes by sentiment and topics
    st.divider()
    st.subheader("Positive / Negative Themes")
    themes = ReviewService.get_theme_by_sentiment(top_n=8)
    if themes:
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Positive themes**")
            if themes.get("positive") is not None:
                st.dataframe(themes.get("positive"), use_container_width=True)
            else:
                st.info("No positive themes found")
        with col2:
            st.write("**Negative themes**")
            if themes.get("negative") is not None:
                st.dataframe(themes.get("negative"), use_container_width=True)
            else:
                st.info("No negative themes found")

    st.divider()
    st.subheader("Extracted Topics (Lightweight LSA)")
    topics = ReviewService.extract_topics(n_topics=5, n_top_words=6)
    if topics:
        for t in topics:
            st.write(f"**Topic {t['topic_id']}**: " + ", ".join(t["terms"]))
    else:
        st.info("No topics extracted")

    st.divider()

    # Interactive search and filtering
    st.subheader("Search & Filter Reviews")
    with st.form(key="review-search-form"):
        search_text = st.text_input(
            "Search reviews",
            placeholder="Search review text for keywords, phrases, or issues",
        )
        min_rating = st.slider(
            "Minimum Rating",
            min_value=1,
            max_value=5,
            value=3,
            step=1,
        )
        sentiment_choice = st.selectbox(
            "Sentiment",
            options=["All", "Positive", "Neutral", "Negative"],
        )
        submitted = st.form_submit_button("Apply Filters")

    filtered_reviews = ReviewService.filter_reviews(
        search_text, min_rating, sentiment_choice
    )

    st.write(
        f"Showing **{len(filtered_reviews)}** reviews matching the criteria. "
        f"Use search terms and rating filters to narrow down the feedback."
    )

    if len(filtered_reviews) == 0:
        st.info("No reviews match the selected filters.")
    else:
        st.dataframe(
            filtered_reviews[["Review", "Label", "Sentiment", "Review Length"]].head(100),
            hide_index=True,
            use_container_width=True,
        )

        # Export filtered reviews
        csv_bytes = get_filtered_reviews_csv(filtered_reviews)
        if csv_bytes is not None:
            st.download_button("Download filtered reviews (CSV)", data=csv_bytes, file_name="filtered_reviews.csv", mime="text/csv")

    st.divider()
    st.caption(
        "Review Intelligence is intentionally focused on descriptive analytics and simple theme extraction in Phase 2. "
        "Advanced AI insights will be added later."
    )
