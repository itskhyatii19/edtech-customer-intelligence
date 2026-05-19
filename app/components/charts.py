"""Reusable Plotly chart components"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List
from app.config import COLORS, CHURN_RISK_COLORS, SEGMENTS


def engagement_histogram(
    engagement_data: Dict[str, int],
    title: str = "Engagement Score Distribution",
) -> go.Figure:
    """
    Create histogram of engagement score distribution
    
    Args:
        engagement_data: Dict mapping engagement range labels to counts
        title: Chart title
        
    Returns:
        Plotly Figure object
    """
    labels = list(engagement_data.keys())
    values = list(engagement_data.values())

    fig = go.Figure(
        data=[
            go.Bar(
                x=labels,
                y=values,
                marker=dict(color=COLORS["primary"]),
                text=values,
                textposition="auto",
            )
        ]
    )

    fig.update_layout(
        title=title,
        xaxis_title="Engagement Score Range",
        yaxis_title="Number of Users",
        showlegend=False,
        height=400,
        hovermode="x unified",
        template="plotly_white",
    )

    return fig


def inactivity_histogram(
    inactivity_data: Dict[str, int],
    title: str = "Inactivity Distribution",
) -> go.Figure:
    """
    Create histogram of inactivity days distribution
    
    Args:
        inactivity_data: Dict mapping inactivity range labels to counts
        title: Chart title
        
    Returns:
        Plotly Figure object
    """
    labels = list(inactivity_data.keys())
    values = list(inactivity_data.values())

    fig = go.Figure(
        data=[
            go.Bar(
                x=labels,
                y=values,
                marker=dict(color=COLORS["warning"]),
                text=values,
                textposition="auto",
            )
        ]
    )

    fig.update_layout(
        title=title,
        xaxis_title="Days Inactive",
        yaxis_title="Number of Users",
        showlegend=False,
        height=400,
        hovermode="x unified",
        template="plotly_white",
    )

    return fig


def segment_pie_chart(
    segment_data: Dict[str, int],
    title: str = "User Segments",
) -> go.Figure:
    """
    Create pie chart of user segments
    
    Args:
        segment_data: Dict mapping segment names to user counts
        title: Chart title
        
    Returns:
        Plotly Figure object
    """
    # Map segment names to display labels and colors
    labels = []
    values = []
    colors = []

    for segment_key, count in segment_data.items():
        if segment_key in SEGMENTS:
            labels.append(SEGMENTS[segment_key]["label"])
            colors.append(SEGMENTS[segment_key]["color"])
        else:
            labels.append(segment_key.replace("_", " ").title())
            colors.append(COLORS["neutral"])
        values.append(count)

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                marker=dict(colors=colors),
                textposition="inside",
                textinfo="label+percent",
            )
        ]
    )

    fig.update_layout(
        title=title,
        height=400,
        template="plotly_white",
    )

    return fig


def churn_distribution_chart(
    churn_data: Dict[str, int],
    title: str = "Churn Risk Distribution",
) -> go.Figure:
    """
    Create pie chart of churn risk distribution
    
    Args:
        churn_data: Dict mapping churn risk levels to user counts
        title: Chart title
        
    Returns:
        Plotly Figure object
    """
    labels = list(churn_data.keys())
    values = list(churn_data.values())

    # Map churn levels to colors
    colors = [CHURN_RISK_COLORS.get(risk.lower(), COLORS["neutral"]) for risk in labels]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                marker=dict(colors=colors),
                textposition="inside",
                textinfo="label+percent",
            )
        ]
    )

    fig.update_layout(
        title=title,
        height=400,
        template="plotly_white",
    )

    return fig


def top_reviewers_chart(
    reviewers_df: pd.DataFrame,
    title: str = "Top Reviewers",
) -> go.Figure:
    """
    Create horizontal bar chart of top reviewers
    
    Args:
        reviewers_df: DataFrame with 'Reviewer' and 'Review Count' columns
        title: Chart title
        
    Returns:
        Plotly Figure object
    """
    if reviewers_df is None or len(reviewers_df) == 0:
        # Return empty figure if no data
        fig = go.Figure()
        fig.add_annotation(text="No reviewer data available")
        return fig

    fig = go.Figure(
        data=[
            go.Bar(
                y=reviewers_df.iloc[::-1]["Reviewer"],
                x=reviewers_df.iloc[::-1]["Review Count"],
                orientation="h",
                marker=dict(color=COLORS["secondary"]),
                text=reviewers_df.iloc[::-1]["Review Count"],
                textposition="auto",
            )
        ]
    )

    fig.update_layout(
        title=title,
        xaxis_title="Number of Reviews",
        yaxis_title="Reviewer",
        showlegend=False,
        height=400,
        hovermode="y unified",
        template="plotly_white",
    )

    return fig


def rating_histogram(
    rating_distribution: Dict[float, int],
    title: str = "Rating Distribution",
) -> go.Figure:
    """Create a bar chart for rating distribution."""
    labels = [str(int(k)) for k in sorted(rating_distribution.keys())]
    values = [rating_distribution[k] for k in sorted(rating_distribution.keys())]

    fig = go.Figure(
        data=[
            go.Bar(
                x=labels,
                y=values,
                marker=dict(color=COLORS["primary"]),
                text=values,
                textposition="auto",
            )
        ]
    )

    fig.update_layout(
        title=title,
        xaxis_title="Rating",
        yaxis_title="Review Count",
        showlegend=False,
        height=400,
        hovermode="x unified",
        template="plotly_white",
    )
    return fig


def retention_curve_chart(
    retention_data: Dict[str, float],
    title: str = "Retention Curve",
) -> go.Figure:
    """Create a retention curve chart from binned retention data."""
    labels = list(retention_data.keys())
    values = list(retention_data.values())

    fig = go.Figure(
        data=[
            go.Scatter(
                x=labels,
                y=values,
                mode="lines+markers",
                line=dict(color=COLORS["primary"], width=3),
                marker=dict(size=8),
            )
        ]
    )

    fig.update_layout(
        title=title,
        xaxis_title="Days Since Last Activity",
        yaxis_title="Share of Users (%)",
        height=400,
        hovermode="x unified",
        template="plotly_white",
    )
    return fig


def activity_frequency_histogram(
    activity_data: Dict[str, int],
    title: str = "Activity Frequency",
) -> go.Figure:
    """Create a histogram chart for activity frequency."""
    labels = list(activity_data.keys())
    values = list(activity_data.values())

    fig = go.Figure(
        data=[
            go.Bar(
                x=labels,
                y=values,
                marker=dict(color=COLORS["secondary"]),
                text=values,
                textposition="auto",
            )
        ]
    )

    fig.update_layout(
        title=title,
        xaxis_title="Activity Range",
        yaxis_title="Number of Users",
        showlegend=False,
        height=400,
        hovermode="x unified",
        template="plotly_white",
    )
    return fig


def engagement_inactivity_scatter(
    df: pd.DataFrame,
    title: str = "Engagement vs Inactivity",
) -> go.Figure:
    """Create a scatter plot comparing engagement score and inactivity."""
    fig = px.scatter(
        df,
        x="inactive_days",
        y="engagement_score",
        color="churn_risk",
        color_discrete_map=CHURN_RISK_COLORS,
        hover_data={"uuid": True, "user_segment": True, "activity_count": True},
        labels={
            "inactive_days": "Days Inactive",
            "engagement_score": "Engagement Score",
            "churn_risk": "Churn Risk",
        },
        title=title,
        height=420,
    )
    fig.update_traces(marker=dict(size=8, opacity=0.8))
    fig.update_layout(template="plotly_white", hovermode="closest")
    return fig


def sentiment_bar_chart(
    sentiment_data: Dict[str, int],
    title: str = "Sentiment Distribution",
) -> go.Figure:
    """Create a bar chart for sentiment categories."""
    labels = list(sentiment_data.keys())
    values = list(sentiment_data.values())
    colors = [
        COLORS["success"] if label == "Positive" else COLORS["neutral"] if label == "Neutral" else COLORS["warning"] if label == "Negative" else COLORS["primary"]
        for label in labels
    ]

    fig = go.Figure(
        data=[
            go.Bar(
                x=labels,
                y=values,
                marker=dict(color=colors),
                text=values,
                textposition="auto",
            )
        ]
    )

    fig.update_layout(
        title=title,
        xaxis_title="Sentiment",
        yaxis_title="Review Count",
        showlegend=False,
        height=400,
        hovermode="x unified",
        template="plotly_white",
    )
    return fig


def keyword_bar_chart(
    keyword_df: pd.DataFrame,
    title: str = "Top Review Themes",
) -> go.Figure:
    """Create a horizontal bar chart for top review keywords."""
    if keyword_df is None or keyword_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No keyword data available")
        return fig

    keyword_column = "Keyword" if "Keyword" in keyword_df.columns else keyword_df.columns[0]
    count_column = None
    for candidate in ["Count", "Score", keyword_df.columns[1] if len(keyword_df.columns) > 1 else None]:
        if candidate is not None and candidate in keyword_df.columns:
            count_column = candidate
            break

    if count_column is None:
        fig = go.Figure()
        fig.add_annotation(text="Keyword frequency column not found")
        return fig

    x_values = keyword_df[count_column].tolist()[::-1]
    y_values = keyword_df[keyword_column].astype(str).tolist()[::-1]
    text_values = [f"{v:.2f}" if isinstance(v, float) else str(v) for v in x_values]

    fig = go.Figure(
        data=[
            go.Bar(
                x=x_values,
                y=y_values,
                orientation="h",
                marker=dict(color=COLORS["secondary"]),
                text=text_values,
                textposition="auto",
            )
        ]
    )

    fig.update_layout(
        title=title,
        xaxis_title="Frequency",
        yaxis_title="Keyword",
        height=450,
        margin=dict(l=180, r=30, t=50, b=40),
        template="plotly_white",
    )
    return fig


def kpi_chart(value: float, title: str, suffix: str = "") -> go.Figure:
    """
    Create a simple KPI indicator
    
    Args:
        value: Metric value (0-100 for gauge)
        title: Chart title
        suffix: Value suffix (e.g., '%', 'days')
        
    Returns:
        Plotly Figure object
    """
    fig = go.Figure(
        data=[
            go.Indicator(
                mode="gauge+number+delta",
                value=value,
                title={"text": title},
                domain={"x": [0, 1], "y": [0, 1]},
                gauge={
                    "axis": {"range": [None, 100]},
                    "bar": {"color": COLORS["primary"]},
                    "steps": [
                        {"range": [0, 33], "color": "lightgray"},
                        {"range": [33, 67], "color": "gray"},
                    ],
                    "threshold": {
                        "line": {"color": "red", "width": 4},
                        "thickness": 0.75,
                        "value": 90,
                    },
                },
                suffix=suffix,
            )
        ]
    )

    fig.update_layout(height=400)
    return fig
