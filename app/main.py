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

from app.config import (
    APP_TITLE,
    APP_DESCRIPTION,
    APP_ICON,
    APP_VERSION,
    APP_AUTHOR,
    APP_COPYRIGHT,
    APP_PAGES,
)
from app.pages import (
    render_home,
    render_ai_insights,
    render_learner_analytics,
    render_review_intelligence,
    render_settings,
)

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
        **Version:** {APP_VERSION}  
        **Author:** {APP_AUTHOR}  
        **Copyright:** {APP_COPYRIGHT}
        """
    },
)

# ============================================================================
# Custom Styling
# ============================================================================
st.markdown(
    """
    <style>
        #MainMenu, footer {
            visibility: hidden;
        }
        .stApp {
            background-color: #f8fafc;
        }
        .block-container {
            padding-top: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        .stButton>button {
            border-radius: 0.75rem;
        }
        .css-1dq8tca {
            padding: 1rem 1rem 0.5rem 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================================
# Sidebar Navigation
# ============================================================================
if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Home"

if st.session_state["selected_page"] not in APP_PAGES:
    st.session_state["selected_page"] = APP_PAGES[0]

with st.sidebar:
    st.title(f"{APP_ICON} Dashboard")
    st.write(APP_DESCRIPTION)
    st.divider()

    selected_page = st.radio(
        "Select a page",
        options=APP_PAGES,
        index=APP_PAGES.index(st.session_state["selected_page"]),
        label_visibility="collapsed",
    )
    st.session_state["selected_page"] = selected_page

    st.divider()
    st.markdown(
        """
        **Quick actions**  
        - Home overview  
        - Learner analytics  
        - AI insights  
        - Review intelligence  
        - Settings
        """
    )
    st.divider()
    st.caption("Data updates every hour. Use Settings to refresh cache.")

# ============================================================================
# Page Routing
# ============================================================================
PAGE_RENDERERS = {
    "Home": render_home,
    "Learner Analytics": render_learner_analytics,
    "AI Insights": render_ai_insights,
    "Review Intelligence": render_review_intelligence,
    "Settings": render_settings,
}

render_page = PAGE_RENDERERS.get(selected_page, render_home)
render_page()

st.divider()
st.caption(f"{APP_TITLE} · {APP_VERSION} · {APP_COPYRIGHT}")
