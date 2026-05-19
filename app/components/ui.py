"""Reusable UI helpers for the Streamlit dashboard."""

from typing import Iterable, Mapping, Optional

import streamlit as st


def page_container():
    """Return a container for page sections."""
    return st.container()


def section_header(title: str, subtitle: Optional[str] = None) -> None:
    """Render a compact page section header."""
    st.markdown(
        f"""
        <div style='margin-bottom:0.85rem;'>
            <h1 style='margin:0; padding:0; font-size:1.75rem; line-height:1.15; letter-spacing:-0.03em; color:#0f172a;'>{title}</h1>
            {f'<p style="margin:0.35rem 0 0 0; color:#475569; font-size:0.95rem; max-width:92%;">{subtitle}</p>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(title: str, subtitle: Optional[str] = None) -> None:
    """Render a page title, subtitle, and top divider section."""
    with page_container():
        st.title(title)
        if subtitle:
            st.markdown(
                f"""
                <div style='margin-top:-0.5rem; color:#475569; font-size:0.95rem; max-width:92%;'>
                    {subtitle}
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.divider()


def metric_card(
    title: str,
    value: str,
    caption: Optional[str] = None,
    delta: Optional[str] = None,
    badge: Optional[str] = None,
) -> None:
    """Render a compact metric card for KPI rows."""
    card_style = (
        "padding:16px; border-radius:16px; background:#ffffff; "
        "border:1px solid #e2e8f0; min-height:128px; display:flex; "
        "flex-direction:column; justify-content:space-between;"
    )
    badge_style = (
        "font-size:0.78rem; color:#64748b; text-transform:uppercase; "
        "letter-spacing:0.08em; margin-bottom:0.4rem;"
    )
    title_style = "font-size:0.95rem; font-weight:700; color:#0f172a; margin-bottom:0.4rem;"
    value_style = "font-size:1.95rem; font-weight:700; color:#0f172a;"
    delta_style = "margin-top:0.5rem; font-size:0.88rem; color:#334155;"
    caption_style = "margin-top:0.8rem; color:#64748b; font-size:0.88rem;"

    html_parts = [
        f"<div style='{card_style}'>",
        "<div>",
    ]

    if badge:
        html_parts.append(f"<div style='{badge_style}'>{badge}</div>")

    html_parts.append(f"<div style='{title_style}'>{title}</div>")
    html_parts.append(f"<div style='{value_style}'>{value}</div>")
    html_parts.append("</div>")

    if delta:
        html_parts.append(f"<div style='{delta_style}'>{delta}</div>")

    if caption:
        html_parts.append(f"<div style='{caption_style}'>{caption}</div>")

    html_parts.append("</div>")
    st.markdown("".join(html_parts), unsafe_allow_html=True)


def info_banner(message: str, variant: str = "info") -> None:
    """Render a small info banner with a subtle background."""
    colors = {
        "info": ("#eff6ff", "#1e40af"),
        "success": ("#ecfdf5", "#166534"),
        "warning": ("#fef3c7", "#92400e"),
        "error": ("#fee2e2", "#991b1b"),
    }
    background, text = colors.get(variant, colors["info"])
    st.markdown(
        f"""
        <div style='padding:0.85rem 1rem; border-radius:14px; background:{background}; border:1px solid rgba(15,23,42,0.08); color:{text}; margin-bottom:1rem;'>
            {message}
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_state(message: str, help_text: Optional[str] = None, icon: str = "ℹ️") -> None:
    """Render a consistent empty-state callout."""
    help_html = f'<div style="margin-top:0.35rem; font-size:0.92rem; color:#475569;">{help_text}</div>' if help_text else ""
    st.markdown(
        f"""
        <div style='padding:18px 20px; border-radius:16px; background:#f8fafc; border:1px solid #dbeafe; color:#0f172a; margin-bottom:1rem;'>
            <div style='font-size:1rem; font-weight:600; margin-bottom:0.35rem;'>{icon} {message}</div>
            {help_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_insight_cards(insights: Iterable[Mapping[str, str]], columns: int = 2) -> None:
    """Render a set of insight cards in a compact grid."""
    cols = st.columns(columns, gap="large")
    insights_list = list(insights)
    for index, insight in enumerate(insights_list):
        with cols[index % columns]:
            st.markdown(
                f"""
                <div style='padding:18px; border-radius:16px; background:#f8fafc; border:1px solid #e2e8f0; min-height:128px;'>
                    <div style='font-weight:700; color:#0f172a; margin-bottom:0.65rem; font-size:0.98rem;'>{insight.get('title', 'Insight')}</div>
                    <div style='color:#475569; font-size:0.92rem; line-height:1.55;'>{insight.get('detail', '')}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# Backwards-compatible aliases
section_title = section_header
render_section_title = section_header
render_section_header = section_header
render_dashboard_card = metric_card
render_empty_state = empty_state
