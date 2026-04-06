"""
Chart Styling and Utilities
Handles all chart configuration and styling for consistency.
"""

import streamlit as st
from typing import Dict
import plotly.graph_objects as go
import plotly.express as px


def get_chart_theme() -> Dict:
    """Get chart theme based on current dark mode setting
    
    Returns:
        Dictionary with chart theme colors
    """
    dark = st.session_state.get("dark_mode", True)
    
    return {
        "paper_bg": "rgba(0,0,0,0)",
        "plot_bg": "rgba(0,0,0,0)",
        "font_color": "#6B9478" if dark else "#3D6E54",
        "grid_color": "#1A2E22" if dark else "#C8E6D4",
        "line_color": "#1A2E22" if dark else "#C8E6D4",
        "accent": "#00D98A" if dark else "#00A86B",
        "accent2": "#FFB020" if dark else "#D4890A",
    }


def style_figure(fig: go.Figure, height: int = 300) -> go.Figure:
    """Apply consistent styling to a Plotly figure
    
    Args:
        fig: Plotly figure to style
        height: Figure height in pixels
        
    Returns:
        Styled figure
    """
    theme = get_chart_theme()
    
    fig.update_layout(
        paper_bgcolor=theme["paper_bg"],
        plot_bgcolor=theme["plot_bg"],
        font=dict(
            color=theme["font_color"],
            family="Plus Jakarta Sans",
            size=11
        ),
        height=height,
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(size=10)
        ),
        xaxis=dict(
            gridcolor=theme["grid_color"],
            linecolor=theme["line_color"],
            showgrid=True
        ),
        yaxis=dict(
            gridcolor=theme["grid_color"],
            linecolor=theme["line_color"],
            showgrid=True
        ),
    )
    
    return fig


def style_bar_chart(fig: go.Figure, height: int = 300, 
                   show_labels: bool = True) -> go.Figure:
    """Style a bar chart with standard formatting
    
    Args:
        fig: Plotly bar figure
        height: Figure height
        show_labels: Whether to show value labels on bars
        
    Returns:
        Styled bar chart
    """
    fig = style_figure(fig, height)
    
    if show_labels:
        fig.update_traces(textposition='outside')
    
    fig.update_xaxes(tickangle=-30)
    return fig


def style_line_chart(fig: go.Figure, height: int = 300) -> go.Figure:
    """Style a line chart with standard formatting
    
    Args:
        fig: Plotly line figure
        height: Figure height
        
    Returns:
        Styled line chart
    """
    fig = style_figure(fig, height)
    fig.update_traces(hovertemplate='<b>%{x}</b><br>%{y}<extra></extra>')
    return fig


def style_pie_chart(fig: go.Figure, height: int = 320, 
                   show_percentage: bool = True) -> go.Figure:
    """Style a pie chart with standard formatting
    
    Args:
        fig: Plotly pie figure
        height: Figure height
        show_percentage: Whether to show percentage labels
        
    Returns:
        Styled pie chart
    """
    fig = style_figure(fig, height)
    
    if show_percentage:
        fig.update_traces(textinfo='label+percent')
    else:
        fig.update_traces(textinfo='label')
    
    return fig


def create_time_series_chart(dates: list, values: list, title: str = "",
                            y_label: str = "Value", height: int = 300) -> go.Figure:
    """Create a styled time series line chart
    
    Args:
        dates: List of dates
        values: List of values
        title: Chart title
        y_label: Y-axis label
        height: Chart height
        
    Returns:
        Styled Plotly figure
    """
    theme = get_chart_theme()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=values,
        mode='lines',
        name=y_label,
        line=dict(color=theme["accent"], width=2),
        fill='tozeroy',
        fillcolor=f"rgba(0,217,138,0.1)"
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title=y_label,
        hovermode='x unified',
    )
    
    return style_figure(fig, height)


def create_comparison_chart(categories: list, values1: list, values2: list,
                           label1: str = "Series 1", label2: str = "Series 2",
                           title: str = "", height: int = 300) -> go.Figure:
    """Create a grouped bar chart for comparison
    
    Args:
        categories: List of category names
        values1: First series values
        values2: Second series values
        label1: Label for first series
        label2: Label for second series
        title: Chart title
        height: Chart height
        
    Returns:
        Styled Plotly figure
    """
    theme = get_chart_theme()
    
    fig = go.Figure(data=[
        go.Bar(name=label1, x=categories, y=values1,
               marker_color=theme["accent"]),
        go.Bar(name=label2, x=categories, y=values2,
               marker_color=theme["accent2"]),
    ])
    
    fig.update_layout(
        barmode='group',
        title=title,
        xaxis_title="Category",
        yaxis_title="Value",
    )
    
    return style_figure(fig, height)


def get_color_sequence() -> list:
    """Get consistent color sequence for charts
    
    Returns:
        List of colors for use in charts
    """
    return [
        "#00D98A",  # Green/accent
        "#FFB020",  # Orange/accent2
        "#34D399",  # Light green
        "#60A5FA",  # Light blue
        "#A78BFA",  # Light purple
        "#FB7185",  # Light red
        "#FBBF24",  # Light yellow
        "#10B981",  # Dark green
    ]


def render_chart_with_controls(fig: go.Figure, key_prefix: str = "") -> None:
    """Render a chart with download and theme controls
    
    Args:
        fig: Plotly figure to render
        key_prefix: Prefix for widget keys (for uniqueness)
    """
    col1, col2 = st.columns([1, 0.2])
    
    with col1:
        st.plotly_chart(fig, use_container_width=True, 
                       config={"displayModeBar": False})
    
    with col2:
        if st.button("📥 Download", key=f"dl_{key_prefix}"):
            # Note: Actual download would require additional implementation
            st.info("Download feature coming soon")
