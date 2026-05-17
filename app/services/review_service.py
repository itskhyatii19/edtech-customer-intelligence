"""Reusable service for review analytics and search."""

import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from app.services.data_loader import DataLoader
import nltk
from nltk.corpus import stopwords
import re

# Ensure NLTK resources are available; download if missing
try:
    _ = stopwords.words("english")
except Exception:
    nltk.download("stopwords")
    _ = stopwords.words("english")

EN_STOPWORDS = set(stopwords.words("english"))
EN_STOPWORDS_LIST = list(EN_STOPWORDS)

def _clean_text(text: str) -> str:
    """Basic text cleanup: lowercase, remove non-word chars, collapse whitespace."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


class ReviewService:
    """Review analytics service used by the dashboard."""

    @staticmethod
    @st.cache_data(ttl=3600)
    def load_reviews():
        """Load review data from storage and return a DataFrame."""
        reviews = DataLoader.load_reviews()
        if reviews is None:
            return None

        reviews = reviews.copy()
        reviews["Review"] = reviews["Review"].astype(str).str.strip()
        if "Label" in reviews.columns:
            reviews["Label"] = pd.to_numeric(reviews["Label"], errors="coerce")
        
        reviews["Sentiment"] = reviews["Label"].apply(ReviewService._map_rating_to_sentiment)
        reviews["Review Length"] = reviews["Review"].str.len()
        return reviews

    @staticmethod
    def _map_rating_to_sentiment(rating):
        """Map review rating to a simple sentiment category."""
        try:
            rating = float(rating)
        except (TypeError, ValueError):
            return "Unknown"

        if rating >= 4:
            return "Positive"
        if rating == 3:
            return "Neutral"
        if rating <= 2:
            return "Negative"
        return "Unknown"

    @staticmethod
    @st.cache_data(ttl=3600)
    def get_review_statistics():
        """Return summary statistics for review data."""
        reviews = ReviewService.load_reviews()
        if reviews is None:
            return {}

        stats = {
            "total_reviews": len(reviews),
            "avg_rating": float(reviews["Label"].mean()) if "Label" in reviews.columns else None,
            "median_rating": float(reviews["Label"].median()) if "Label" in reviews.columns else None,
            "positive_reviews": int((reviews["Sentiment"] == "Positive").sum()),
            "neutral_reviews": int((reviews["Sentiment"] == "Neutral").sum()),
            "negative_reviews": int((reviews["Sentiment"] == "Negative").sum()),
        }

        return stats

    @staticmethod
    @st.cache_data(ttl=3600)
    def get_rating_distribution():
        """Return a distribution of ratings for Plotly charts."""
        reviews = ReviewService.load_reviews()
        if reviews is None or "Label" not in reviews.columns:
            return {}

        distribution = reviews["Label"].value_counts().sort_index()
        return distribution.to_dict()

    @staticmethod
    @st.cache_data(ttl=3600)
    def get_sentiment_distribution():
        """Return counts of sentiment classes for visualization."""
        reviews = ReviewService.load_reviews()
        if reviews is None:
            return {}

        distribution = reviews["Sentiment"].value_counts().reindex(
            ["Positive", "Neutral", "Negative"], fill_value=0
        )
        return distribution.to_dict()

    @staticmethod
    @st.cache_data(ttl=3600)
    def get_top_keywords(n=12):
        """Return the top keywords/themes using TF-IDF and n-grams.

        This uses a TF-IDF vectorizer to surface high-importance n-grams,
        filtered by English stopwords and document frequency thresholds.
        """
        reviews = ReviewService.load_reviews()
        if reviews is None:
            return None

        text_series = reviews["Review"].dropna().astype(str).map(_clean_text)

        vectorizer = TfidfVectorizer(
            stop_words=EN_STOPWORDS_LIST,
            ngram_range=(1, 2),
            max_df=0.85,
            min_df=5,
            max_features=500,
        )

        tfidf = vectorizer.fit_transform(text_series)
        scores = tfidf.sum(axis=0).A1
        terms = vectorizer.get_feature_names_out()

        freq_df = pd.DataFrame({"Keyword": terms, "Score": scores})
        freq_df = freq_df.sort_values("Score", ascending=False).head(n)
        return freq_df

    @staticmethod
    @st.cache_data(ttl=3600)
    def get_theme_by_sentiment(top_n=10):
        """Return top themes separately for positive and negative reviews."""
        reviews = ReviewService.load_reviews()
        if reviews is None:
            return {"positive": None, "negative": None}

        pos = reviews[reviews["Sentiment"] == "Positive"]["Review"].dropna().astype(str).map(_clean_text)
        neg = reviews[reviews["Sentiment"] == "Negative"]["Review"].dropna().astype(str).map(_clean_text)

        def _top_for_series(series, n=top_n):
            if series.empty:
                return None
            v = TfidfVectorizer(stop_words=EN_STOPWORDS_LIST, ngram_range=(1, 2), max_df=0.9, min_df=3, max_features=300)
            tf = v.fit_transform(series)
            scores = tf.sum(axis=0).A1
            terms = v.get_feature_names_out()
            df = pd.DataFrame({"Keyword": terms, "Score": scores}).sort_values("Score", ascending=False).head(n)
            return df

        return {"positive": _top_for_series(pos), "negative": _top_for_series(neg)}

    @staticmethod
    @st.cache_data(ttl=3600)
    def extract_topics(n_topics=5, n_top_words=8):
        """Extract lightweight topics using TF-IDF + TruncatedSVD (LSA).

        Returns a list of topic dictionaries with top words.
        """
        reviews = ReviewService.load_reviews()
        if reviews is None:
            return None

        texts = reviews["Review"].dropna().astype(str).map(_clean_text)
        if texts.empty:
            return None

        v = TfidfVectorizer(stop_words=EN_STOPWORDS_LIST, ngram_range=(1, 2), max_df=0.9, min_df=5, max_features=2000)
        tf = v.fit_transform(texts)

        svd = TruncatedSVD(n_components=n_topics, random_state=42)
        svd.fit(tf)

        terms = v.get_feature_names_out()
        topics = []
        for i, comp in enumerate(svd.components_):
            terms_idx = comp.argsort()[::-1][:n_top_words]
            topics.append({"topic_id": i, "terms": [terms[t] for t in terms_idx]})

        return topics

    @staticmethod
    def filter_reviews(search_text: str = "", min_rating: int = 1, sentiment: str = "All"):
        """Filter review records based on keyword, rating, and sentiment."""
        reviews = ReviewService.load_reviews()
        if reviews is None:
            return None

        filtered = reviews.copy()
        if min_rating is not None and "Label" in filtered.columns:
            filtered = filtered[filtered["Label"] >= min_rating]

        if sentiment and sentiment != "All":
            filtered = filtered[filtered["Sentiment"] == sentiment]

        if search_text:
            term = str(search_text).strip().lower()
            filtered = filtered[filtered["Review"].str.lower().str.contains(term, na=False)]

        return filtered.sort_values(by="Label", ascending=False).reset_index(drop=True)
