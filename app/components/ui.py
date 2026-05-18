"""Reusable UI helpers for the Streamlit dashboard."""

from typing import Iterable, Mapping, Optional

import streamlit as st


def render_section_title(title: str, subtitle: Optional[str] = None) -> None:
    """Render a polished section title with optional subtitle."""
    st.markdown(f"## {title}")
    if subtitle:
        st.write(subtitle)


def render_dashboard_card(
    title: str,
    value: str,
    caption: Optional[str] = None,
    delta: Optional[str] = None,
    badge: Optional[str] = None,
) -> None:
    """Render a compact dashboard card with consistent spacing."""
    badge_markup = f"<span style='font-size:0.8rem;color:#6b7280'>{badge}</span><br>" if badge else ""
    delta_markup = f"<div style='margin-top:0.5rem;color:#475569;font-size:0.9rem'>{delta}</div>" if delta else ""
    st.markdown(
        f"""
        <div style="padding:18px; border-radius:16px; background:#ffffff; box-shadow:0 8px 24px rgba(15,23,42,0.06); min-height:128px;">
            <div style="font-size:0.82rem; color:#64748b; letter-spacing:0.02em; text-transform:uppercase;">{badge_markup if badge else ''}</div>
            <div style="font-size:0.95rem; color:#475569; margin-bottom:0.5rem;">{title}</div>
            <div style="font-size:2rem; font-weight:700; color:#0f172a;">{value}</div>
            {delta_markup}
            {f'<div style="margin-top:0.8rem; color:#64748b; font-size:0.88rem;">{caption}</div>' if caption else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


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
            st.markdown(
                f"""
                <div style="padding:18px; border-radius:16px; background:#f8fafc; border:1px solid #e2e8f0; min-height:108px;">
                    <div style="font-weight:700; color:#0f172a; margin-bottom:8px;">{insight.get('title', 'Insight')}</div>
                    <div style="color:#475569; font-size:0.92rem; line-height:1.5;">{insight.get('detail', '')}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_navigation_card(title: str, description: str, page_name: str, key: str) -> None:
    """Render a small navigation card that updates the active page."""
    st.markdown(
        f"""
        <div style="padding:18px; border-radius:16px; background:#ffffff; box-shadow:0 8px 24px rgba(15,23,42,0.06); min-height:140px; display:flex; flex-direction:column; justify-content:space-between;">
            <div>
                <div style='font-size:0.95rem; font-weight:700; color:#0f172a; margin-bottom:8px;'>{title}</div>
                <div style='color:#475569; font-size:0.92rem; line-height:1.5;'>{description}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(f"Open {title}", key=key, use_container_width=True):
        st.session_state["selected_page"] = page_name
        st.experimental_rerun()
