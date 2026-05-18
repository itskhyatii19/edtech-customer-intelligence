"""Reusable UI helpers for the Streamlit dashboard."""

from typing import Iterable, Mapping, Optional

import streamlit as st


def render_section_title(title: str, subtitle: Optional[str] = None) -> None:
    """Render a polished section title with optional subtitle."""
    st.markdown(f"### {title}")
    if subtitle:
        st.write(subtitle)


def render_empty_state(message: str, help_text: Optional[str] = None, icon: str = "⚠️") -> None:
    """Render a consistent empty-state callout."""
    st.info(f"{icon} {message}")
    if help_text:
        st.caption(help_text)


def render_insight_cards(insights: Iterable[Mapping[str, str]], columns: int = 2) -> None:
    """Render a set of insight cards in a compact grid."""
    cols = st.columns(columns)
    insights_list = list(insights)
    for index, insight in enumerate(insights_list):
        with cols[index % columns]:
            st.info(f"**{insight.get('title', 'Insight')}**\n\n{insight.get('detail', '')}")
