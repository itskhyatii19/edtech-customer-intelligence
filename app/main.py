"""
Main Streamlit application entry point

EdTech Customer Intelligence Platform - Dashboard Application
"""

import streamlit as st
from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.config import APP_TITLE, APP_DESCRIPTION, APP_ICON
from app.pages.home import render_home
from app.pages.review_intelligence import render_review_intelligence
from app.pages.learner_analytics import render_learner_analytics
from app.pages.ai_insights import render_ai_insights
from app.services import ChurnService

# ============================================================================
# Page Configuration
# ============================================================================
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": f"""
        # {APP_TITLE}
        
        {APP_DESCRIPTION}
        
        ---
        **Version:** 0.1.0  
        **Author:** EdTech Analytics Team  
        **Last Updated:** May 2026
        """
    },
)

# ============================================================================
# Custom Styling
# ============================================================================
st.markdown(
    """
    <style>
        /* Hide the default Streamlit menu and footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Custom styling */
        .metric-card {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #f0f2f6;
        }
        .stPlotlyChart > div {
            margin-bottom: 0.5rem;
        }
        .block-container {
            padding-top: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================================
# Sidebar Navigation
# ============================================================================
with st.sidebar:
    st.title(f"{APP_ICON} Navigation")
    st.divider()

    # Navigation menu
    selected_page = st.radio(
        "Go to:",
        options=["Home", "AI Insights", "Learner Analytics", "Review Intelligence", "Settings"],
        label_visibility="collapsed",
    )

    st.divider()

    # Sidebar info
    st.subheader("📊 Dashboard Info")
    with st.expander("About", expanded=False):
        st.write(APP_DESCRIPTION)

    with st.expander("Data Sources", expanded=False):
        st.write(
            """
            - **Users:** Info_UserData.csv
            - **Activity:** Log_Problem.csv
            - **Reviews:** reviews.csv
            - **Limit:** 500K activity logs (most recent)
            """
        )

    with st.expander("Metrics Explained", expanded=False):
        st.write(
            """
            **Engagement Score:** Ratio of user activities to max activities  
            **Churn Risk:** Based on engagement and inactivity thresholds  
            **Segments:** Highly Active (>0.7), Moderate (0.3-0.7), Low Active (<0.3)  
            **Inactive Days:** Days since last platform activity
            """
        )

    st.divider()
    st.caption("💡 Data refreshes every hour. Use Settings to clear cache.")

# ============================================================================
# Page Router
# ============================================================================
if selected_page == "Home":
    render_home()

elif selected_page == "Learner Analytics":
    render_learner_analytics()

elif selected_page == "AI Insights":
    render_ai_insights()

elif selected_page == "Review Intelligence":
    render_review_intelligence()

elif selected_page == "Settings":
    st.title("⚙️ Settings & Data Management")

    with st.expander("Cache Management", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔄 Clear All Cache", use_container_width=True):
                from app.services import clear_all_cache

                clear_all_cache()
                st.success("✅ Cache cleared successfully!")
                st.rerun()

        with col2:
            st.info(
                "ℹ️ Data is cached for 1 hour to improve performance. "
                "Clear to reload immediately."
            )

        st.divider()
        with st.expander("Churn Parameters", expanded=False):
            st.write("Adjust churn scoring weights and thresholds used by the analytics.")
            w_eng = st.slider("Engagement weight", min_value=0.0, max_value=1.0, value=0.5, step=0.05)
            w_inact = st.slider("Inactivity weight", min_value=0.0, max_value=1.0, value=0.3, step=0.05)
            w_freq = st.slider("Frequency weight", min_value=0.0, max_value=1.0, value=0.2, step=0.05)
            low_t = st.slider("Low risk threshold", min_value=0.0, max_value=1.0, value=0.33, step=0.01)
            high_t = st.slider("High risk threshold", min_value=0.0, max_value=1.0, value=0.66, step=0.01)

            if st.button("Recompute churn with these parameters"):
                # Clear cached features and recompute with new churn params
                from app.services import clear_all_cache

                clear_all_cache()
                try:
                    # Trigger recompute
                    from app.services import DataLoader
                    df = DataLoader.load_features()
                    # Recompute using ChurnService with provided weights and thresholds
                    df = ChurnService.compute_and_assign(df, low_thresh=low_t, high_thresh=high_t,
                                                        weight_engagement=w_eng, weight_inactivity=w_inact, weight_frequency=w_freq)
                    st.success("✅ Churn recomputed and cache refreshed")
                except Exception as e:
                    st.error(f"Error recomputing churn: {e}")

        st.divider()
        with st.expander("Cache TTL", expanded=False):
            from app.services import get_cache_ttl_minutes, set_cache_ttl_minutes, clear_all_cache

            cur = get_cache_ttl_minutes()
            ttl_min = st.slider("Cache TTL (minutes)", min_value=5, max_value=1440, value=int(cur), step=5)

            if st.button("Save TTL"):
                set_cache_ttl_minutes(ttl_min)
                st.success(f"Saved cache TTL = {ttl_min} minutes")

            if st.button("Apply TTL and Clear Cache"):
                # Persist and clear cache; note: decorators use static TTL at import time.
                set_cache_ttl_minutes(ttl_min)
                clear_all_cache()
                # Trigger a re-load to populate caches under new workflow
                try:
                    from app.services import DataLoader

                    _ = DataLoader.load_features()
                    st.success("✅ Cache cleared and data reloaded")
                except Exception as e:
                    st.error(f"Error reloading data after clearing cache: {e}")

            st.caption("Note: Changing TTL updates the session setting. To fully apply TTL to cached functions, refactor cache decorators to read this setting.")

    st.divider()

    with st.expander("Data Source Info", expanded=False):
        st.subheader("📁 Data Files")
        st.write(
            """
            Located in `data/` directory:
            - `junyi/raw/Info_UserData.csv` - User demographics
            - `junyi/raw/Log_Problem.csv` - Activity logs (500K limit)
            - `reviews/raw/reviews.csv` - Student reviews
            """
        )

    with st.expander("Feature Engineering Parameters", expanded=False):
        st.subheader("⚙️ Thresholds")
        st.write(
            """
            - **Engagement High Threshold:** 0.7
            - **Engagement Moderate Threshold:** 0.3
            - **Churn Engagement Quantile:** 30th percentile
            - **Churn Inactivity Quantile:** 70th percentile
            - **Max Inactive Days:** 365 days
            """
        )

    st.divider()

    with st.expander("Application Info", expanded=False):
        st.subheader("📋 System Info")
        col1, col2 = st.columns(2)

        with col1:
            st.metric("App Version", "0.1.0")
            st.metric("Phase", "1 - Foundation")

        with col2:
            st.metric("Last Update", "May 2026")
            st.metric("Framework", "Streamlit")

# ============================================================================
# Footer
# ============================================================================
st.divider()
st.caption(
    "EdTech Customer Intelligence Platform | "
    "[GitHub](https://github.com) | "
    "[Report Issue](https://github.com/issues)"
)
