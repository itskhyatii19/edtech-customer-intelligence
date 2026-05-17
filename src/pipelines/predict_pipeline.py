import pandas as pd
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.features.build_features import build_features
from src.llm.insights import generate_summary, extract_insights

def clean_reviews(text_list):
    cleaned = []
    for t in text_list:
        t = str(t).strip()
        if len(t) > 20:  # remove useless short reviews
            cleaned.append(t)
    return " ".join(cleaned[:10])

def run_pipeline():
    print("🔄 Building features...")
    df = build_features()
    print("✅ Done building features")

    # =========================
    # 👤 USER ANALYSIS
    # =========================
    sample_users = df.head(5).to_dict(orient="records")

    # =========================
    # 📊 REVIEW ANALYSIS (LLM)
    # =========================
    print("🔄 Loading reviews...")
    reviews_path = os.path.join(project_root, "data/reviews/raw/reviews.csv")
    reviews = pd.read_csv(reviews_path)

    texts = reviews["Review"].dropna().tolist()
    sample_text = clean_reviews(texts)

    print("🤖 Generating summary...")
    summary = generate_summary(sample_text)

    print("🤖 Extracting insights...")
    insights = extract_insights(sample_text)

    # =========================
    # 🚀 FINAL OUTPUT
    # =========================
    return {
        "user_analysis": sample_users,
        "review_summary": summary,
        "review_insights": insights
    }