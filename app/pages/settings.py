"""Settings page for cache and churn parameter management."""

import streamlit as st
from app.services import ChurnService


def render() -> None:
    st.title("⚙️ Settings & Data Management")
    st.write("Control caching, churn scoring, and data refresh behavior.")

    with st.expander("Cache Management", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear all cache", use_container_width=True):
                from app.services import clear_all_cache

                clear_all_cache()
                st.success("Cache cleared successfully.")
                st.experimental_rerun()
        with col2:
            st.info("Cached data improves app performance for large datasets.")

    st.divider()
    with st.expander("Churn Scoring Parameters", expanded=False):
        st.write("Adjust the weights and thresholds used for churn risk scoring.")
        w_eng = st.slider("Engagement weight", min_value=0.0, max_value=1.0, value=0.5, step=0.05)
        w_inact = st.slider("Inactivity weight", min_value=0.0, max_value=1.0, value=0.3, step=0.05)
        w_freq = st.slider("Frequency weight", min_value=0.0, max_value=1.0, value=0.2, step=0.05)
        low_t = st.slider("Low risk threshold", min_value=0.0, max_value=1.0, value=0.33, step=0.01)
        high_t = st.slider("High risk threshold", min_value=0.0, max_value=1.0, value=0.66, step=0.01)

        if st.button("Recompute churn with parameters"):
            from app.services import clear_all_cache, DataLoader
            clear_all_cache()
            try:
                df = DataLoader.load_features()
                _ = ChurnService.compute_and_assign(
                    df,
                    low_thresh=low_t,
                    high_thresh=high_t,
                    weight_engagement=w_eng,
                    weight_inactivity=w_inact,
                    weight_frequency=w_freq,
                )
                st.success("Churn recomputed and cached successfully.")
            except Exception as e:
                st.error(f"Unable to recompute churn: {e}")

    st.divider()
    with st.expander("Cache TTL", expanded=False):
        from app.services import get_cache_ttl_minutes, set_cache_ttl_minutes, clear_all_cache

        ttl_min = st.slider("Cache TTL (minutes)", min_value=5, max_value=1440, value=int(get_cache_ttl_minutes()), step=5)
        if st.button("Save TTL"):
            set_cache_ttl_minutes(ttl_min)
            st.success(f"Cache TTL set to {ttl_min} minutes.")
        if st.button("Apply TTL and clear cache"):
            set_cache_ttl_minutes(ttl_min)
            clear_all_cache()
            try:
                from app.services import DataLoader
                _ = DataLoader.load_features()
                st.success("Cache cleared and data reloaded.")
            except Exception as e:
                st.error(f"Unable to reload data after clearing cache: {e}")

        st.caption("TTL changes apply on the next cache refresh.")

    st.divider()
    with st.expander("Data Source Overview", expanded=False):
        st.write(
            """
            - `junyi/raw/Info_UserData.csv` — learner demographics
            - `junyi/raw/Log_Problem.csv` — activity records
            - `reviews/raw/reviews.csv` — student feedback
            """
        )

    st.divider()
    st.markdown(
        """
        **Application version:** 0.1.0  
        **Framework:** Streamlit  
        **Last update:** May 2026
        """
    )
