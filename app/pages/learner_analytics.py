"""Learner Analytics page - cohort analysis and engagement trends."""

import streamlit as st
import pandas as pd
import plotly.express as px
from app.services import DataLoader, AnalyticsService
from app.services.export_service import df_to_csv_bytes


def render_learner_analytics():
    """Render the learner analytics page with cohort and engagement visuals."""
    st.title("👥 Learner Analytics")
    st.write("Cohort analysis, retention trends, engagement trends, and top users.")

    df = DataLoader.load_features()
    if df is None:
        st.error("User feature data not available. Check data source and cache.")
        return

    # Filters
    st.sidebar.header("Learner Analytics Filters")
    segment_filter = st.sidebar.multiselect("User Segment", options=df["user_segment"].unique().tolist(), default=df["user_segment"].unique().tolist())
    min_activity = st.sidebar.slider("Min activity count", min_value=0, max_value=int(df["activity_count"].max()), value=0)

    filtered = df[(df["user_segment"].isin(segment_filter)) & (df["activity_count"] >= min_activity)].copy()

    # Top metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Users (filtered)", len(filtered))
    with col2:
        st.metric("Avg Engagement", f"{filtered['engagement_score'].mean():.2%}")
    with col3:
        st.metric("Avg Activities/User", f"{filtered['activity_count'].mean():.1f}")

    st.divider()

    # Engagement trend: average engagement over days_active buckets
    st.subheader("Engagement by Activity Level")
    filtered["activity_bin"] = pd.cut(filtered["activity_count"], bins=[-1,0,1,5,10,50,100,1000], labels=["0","1","2-5","6-10","11-50","51-100","100+"])
    eng_by_bin = filtered.groupby("activity_bin")["engagement_score"].agg(["mean","median","count"]).reset_index()

    fig = px.bar(eng_by_bin, x="activity_bin", y="mean", labels={"mean":"Avg Engagement","activity_bin":"Activity Bin"}, title="Average Engagement by Activity Bin", text="count")
    st.plotly_chart(fig, use_container_width=True)

    # Retention/Inactive comparison
    st.subheader("Inactive Days Distribution")
    fig2 = px.histogram(filtered, x="inactive_days", nbins=50, title="Days Since Last Activity", labels={"inactive_days":"Inactive Days"}, marginal="box")
    st.plotly_chart(fig2, use_container_width=True)

    # Top engaged users
    st.subheader("Top Engaged Users")
    top_users = filtered.sort_values(by=["engagement_score","activity_count"], ascending=False).head(20)
    st.dataframe(top_users[["uuid","engagement_score","activity_count","churn_score","churn_risk"]], use_container_width=True)

    # Export filtered users
    csv_bytes = df_to_csv_bytes(filtered[["uuid","engagement_score","activity_count","churn_score","churn_risk","user_segment"]])
    st.download_button("Download filtered users CSV", data=csv_bytes, file_name="filtered_users.csv", mime="text/csv")

    st.divider()
    st.caption("Use the sidebar filters to drill into segments and activity thresholds.")
