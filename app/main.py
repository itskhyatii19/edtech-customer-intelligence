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
from app.views import (
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
# Minimal stable sidebar styling (no pseudo-elements, no absolute positioning)
# ============================================================================
st.markdown(
    """
    <style>
        /* Hide Streamlit top menu and footer for cleaner look */
        #MainMenu, footer { visibility: hidden; }

        .stApp { background-color: #f8fafc; }
        .block-container { padding-top: 0.75rem; padding-left: 0.75rem; padding-right: 0.75rem; }

        /* Slightly rounded controls */
        .stButton>button { border-radius: 6px; }

        /* Lightweight radio label layout: align icon and text horizontally */
        section[data-testid="stSidebar"] .stRadio { margin-top: 0.25rem; }

        section[data-testid="stSidebar"] .stRadio label {
            display: block !important;
            padding: 6px 8px;
            border-radius: 6px;
            margin-bottom: 6px;
            font-size: 0.95rem;
            font-weight: 600;
            color: #0f172a;
            transition: background 0.12s ease;
        }

        section[data-testid="stSidebar"] .stRadio label:hover { background: #f8fafc; }

        section[data-testid="stSidebar"] .stRadio label > div {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            width: 100%;
        }

        /* Subtle caption styling */
        section[data-testid="stSidebar"] .stCaption { margin-top: 0.2rem; color: #64748b; font-size: 0.82rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================================
# Sidebar Navigation
# ============================================================================
if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Overview"

if st.session_state["selected_page"] not in APP_PAGES:
    st.session_state["selected_page"] = APP_PAGES[0]

with st.sidebar:
    st.markdown(
        f"""
        <div style='padding:0.75rem 0.85rem; border-radius:14px; background:#ffffff; border:1px solid rgba(148,163,184,0.14); margin-bottom:0.75rem;'>
            <div style='font-size:0.98rem; font-weight:800; color:#0f172a; letter-spacing:0.01em; margin-bottom:0.28rem;'>
                EdTech Intelligence
            </div>
            <div style='font-size:0.88rem; line-height:1.45; color:#475569;'>
                {APP_DESCRIPTION}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style='display:flex; align-items:center; justify-content:space-between; margin-bottom:0.35rem;'>
            <div style='font-size:0.92rem; font-weight:700; color:#0f172a;'>Pages</div>
            <div style='font-size:0.78rem; color:#64748b;'>Navigation</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    ICON_MAP = {
        "Overview": "🏠",
        "Learner Analytics": "📊",
        "AI Insights": "💡",
        "Review Intelligence": "📝",
        "Settings": "⚙️",
    }

    selected_page = st.radio(
        "",
        options=APP_PAGES,
        index=APP_PAGES.index(st.session_state["selected_page"]),
        format_func=lambda v: f"{ICON_MAP.get(v, '•')}  {v}",
        label_visibility="collapsed",
    )
    st.session_state["selected_page"] = selected_page

    st.caption("Choose a page from the menu above.")

# ============================================================================
# Page Routing
# ============================================================================
PAGE_RENDERERS = {
    "Overview": render_home,
    "Learner Analytics": render_learner_analytics,
    "AI Insights": render_ai_insights,
    "Review Intelligence": render_review_intelligence,
    "Settings": render_settings,
}

render_page = PAGE_RENDERERS.get(selected_page, render_home)
render_page()

st.divider()
st.caption(f"{APP_TITLE} · {APP_VERSION} · {APP_COPYRIGHT}")
