"""Reusable metric card components"""

import streamlit as st
from typing import Optional


def metric_card(
    label: str,
    value: str,
    delta: Optional[str] = None,
    delta_color: str = "normal",
    help_text: Optional[str] = None,
    col_width: int = 3,
):
    """
    Display a metric card with label and value
    
    Args:
        label: Metric label
        value: Metric value (formatted string)
        delta: Optional change indicator (e.g., "+5%")
        delta_color: Color for delta ('normal', 'inverse', 'off')
        help_text: Tooltip text
        col_width: Column width (1-4)
    """
    with st.container():
        st.metric(
            label=label,
            value=value,
            delta=delta,
            delta_color=delta_color,
            help=help_text,
        )


def metric_row(metrics: list):
    """
    Display multiple metrics in a row
    
    Args:
        metrics: List of dicts with keys:
                - 'label': str
                - 'value': str
                - 'delta': Optional[str]
                - 'delta_color': str (default='normal')
                - 'help': Optional[str]
    """
    cols = st.columns(len(metrics))
    
    for col, metric in zip(cols, metrics):
        with col:
            st.metric(
                label=metric.get("label", ""),
                value=metric.get("value", ""),
                delta=metric.get("delta"),
                delta_color=metric.get("delta_color", "normal"),
                help=metric.get("help"),
            )


def stat_box(label: str, value: str, icon: str = "📊"):
    """
    Display a simple stat box with icon
    
    Args:
        label: Stat label
        value: Stat value
        icon: Emoji icon
    """
    st.write(f"### {icon} {label}")
    st.write(f"**{value}**")
