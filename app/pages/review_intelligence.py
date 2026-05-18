"""Review Intelligence page for student feedback analysis."""

import streamlit as st
from app.services.review_service import ReviewService
from app.components import (
    metric_row,
    rating_histogram,
    sentiment_bar_chart,
    keyword_bar_chart,
    render_empty_state,
    render_section_title,
)
from app.services.export_service import get_filtered_reviews_csv


def render() -> None:
    """Render the review intelligence dashboard page."""
    render_section_title(
        "💬 Review Intelligence",
        "Compare sentiment, ratings, and review themes to prioritize learner feedback improvements.",
    )

    reviews = ReviewService.load_reviews()
    if reviews is None:
        render_empty_state(
            "Unable to load review data.",
            "Check that the review CSV file exists and refresh the app.",
        )
        return

    stats = ReviewService.get_review_statistics()
    metric_row(
        [
            {
                "label": "Total Reviews",
                "value": str(stats.get("total_reviews", 0)),
            },
            {
                "label": "Average Rating",
                "value": f"{stats.get('avg_rating', 0):.2f}" if stats.get("avg_rating") is not None else "N/A",
            },
            {
                "label": "Positive Reviews",
                "value": str(stats.get("positive_reviews", 0)),
            },
            {
                "label": "Negative Reviews",
                "value": str(stats.get("negative_reviews", 0)),
                "delta_color": "inverse",
            },
        ]
    )

    render_section_title("Rating & Sentiment")
    col1, col2 = st.columns(2)
    with col1:
        rating_dist = ReviewService.get_rating_distribution()
        if rating_dist is not None:
            st.plotly_chart(rating_histogram(rating_dist), use_container_width=True)
        else:
            render_empty_state("No rating distribution data available.")
    with col2:
        sentiment_dist = ReviewService.get_sentiment_distribution()
        if sentiment_dist is not None:
            st.plotly_chart(sentiment_bar_chart(sentiment_dist), use_container_width=True)
        else:
            render_empty_state("No sentiment distribution data available.")

    render_section_title("Review Themes")
    st.write("Frequently mentioned themes and keywords identified from review text.")
    top_keywords = ReviewService.get_top_keywords(n=12)
    if top_keywords is not None and not top_keywords.empty:
        st.plotly_chart(keyword_bar_chart(top_keywords), use_container_width=True)
    else:
        render_empty_state("No keyword data available.")

    themes = ReviewService.get_theme_by_sentiment(top_n=8)
    if themes:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Positive themes")
            if themes.get("positive") is not None:
                st.dataframe(themes.get("positive"), use_container_width=True)
            else:
                st.info("No positive themes detected.")
        with col2:
            st.subheader("Negative themes")
            if themes.get("negative") is not None:
                st.dataframe(themes.get("negative"), use_container_width=True)
            else:
                st.info("No negative themes detected.")
    else:
        render_empty_state("No sentiment themes extracted.")

    render_section_title("Topic Extraction")
    topics = ReviewService.extract_topics(n_topics=5, n_top_words=6)
    if topics:
        for topic in topics:
            st.write(f"**Topic {topic['topic_id']}** — {', '.join(topic['terms'])}")
    else:
        render_empty_state("No topics extracted.")

    render_section_title("Search & Filter Reviews")
    with st.expander("Open review filters", expanded=True):
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
            submitted = st.form_submit_button("Apply filters")

        filtered_reviews = ReviewService.filter_reviews(
            search_text, min_rating, sentiment_choice
        )

        st.write(
            f"Showing **{len(filtered_reviews)}** reviews matching the criteria."
        )

        if len(filtered_reviews) == 0:
            st.info("No reviews match the selected filters.")
        else:
            st.dataframe(
                filtered_reviews[["Review", "Label", "Sentiment", "Review Length"]].head(100),
                hide_index=True,
                use_container_width=True,
            )
            csv_bytes = get_filtered_reviews_csv(filtered_reviews)
            if csv_bytes is not None:
                st.download_button(
                    "Download filtered reviews (CSV)",
                    data=csv_bytes,
                    file_name="filtered_reviews.csv",
                    mime="text/csv",
                )

    st.caption(
        "Review Intelligence delivers descriptive analytics and feedback theme summaries for faster action planning."
    )
