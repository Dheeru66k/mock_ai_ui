"""
Utility Helper Functions
Common functions used across the application.
"""

import streamlit as st
import base64
from typing import Dict, List, Any, Optional
from datetime import datetime


def encode_svg_to_base64(svg_str: str) -> str:
    """Encode SVG string to base64"""
    encoded = base64.b64encode(svg_str.strip().encode("utf-8")).decode("utf-8")
    return encoded


def svg_to_img(svg_str: str, size: int = 64) -> str:
    """Convert SVG string to HTML img tag with base64 encoding
    
    Streamlit strips raw <svg> tags, so we use data URIs for safety.
    
    Args:
        svg_str: SVG markup string
        size: Icon size in pixels
        
    Returns:
        HTML img tag with base64 encoded SVG
    """
    encoded = encode_svg_to_base64(svg_str)
    return f'<img src="data:image/svg+xml;base64,{encoded}" width="{size}" height="{size}" style="display:block;">'


def format_currency(value: float) -> str:
    """Format number as USD currency"""
    return f"${value:,.2f}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format number as percentage"""
    return f"{value:.{decimals}f}%"


def format_number(value: float, decimals: int = 0) -> str:
    """Format number with thousands separator"""
    return f"{value:,.{decimals}f}"


def get_status_color(status: str) -> str:
    """Get color for status badge"""
    colors = {
        "active": "#00D98A",
        "inactive": "#FF4D6A",
        "draft": "#FFB020",
        "pending": "#00D98A",
        "approved": "#00D98A",
        "rejected": "#FF4D6A",
    }
    return colors.get(status.lower(), "#FFB020")


def get_status_badge_html(status: str) -> str:
    """Generate HTML for status badge"""
    class_map = {
        "active": "badge-active",
        "inactive": "badge-inactive",
        "draft": "badge-draft",
        "pending": "badge-pending",
        "approved": "badge-active",
        "rejected": "badge-inactive",
    }
    css_class = class_map.get(status.lower(), "badge-draft")
    return f'<span class="badge {css_class}">{status.upper()}</span>'


def format_timestamp(dt: datetime) -> str:
    """Format datetime to readable string"""
    if isinstance(dt, str):
        return dt
    
    now = datetime.now()
    diff = now - dt
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes}m ago" if minutes != 1 else "1m ago"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours}h ago" if hours != 1 else "1h ago"
    elif seconds < 604800:
        days = int(seconds // 86400)
        return f"{days}d ago" if days != 1 else "1d ago"
    else:
        return dt.strftime("%b %d, %Y")


def truncate_text(text: str, length: int = 50) -> str:
    """Truncate text to specified length with ellipsis"""
    if len(text) > length:
        return text[:length-3] + "..."
    return text


def get_initials(name: str) -> str:
    """Get initials from a person's name"""
    parts = name.split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    return name[0].upper() if name else "?"


def generate_metric_card_html(label: str, value: str, delta: Optional[str] = None, 
                             delta_up: bool = True) -> str:
    """Generate HTML for a metric card
    
    Args:
        label: Card label/title
        value: Main metric value
        delta: Change indicator (e.g., "8.1%")
        delta_up: True if positive change, False if negative
        
    Returns:
        HTML string for the metric card
    """
    delta_html = ""
    if delta:
        cls = "delta-up" if delta_up else "delta-down"
        arrow = "↑" if delta_up else "↓"
        delta_html = f'<div class="metric-delta {cls}">{arrow} {delta}</div>'
    
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """


def group_by_key(items: List[Dict], key: str) -> Dict[str, List]:
    """Group list of dictionaries by a key
    
    Args:
        items: List of dictionaries
        key: Key to group by
        
    Returns:
        Dictionary with grouped items
    """
    result = {}
    for item in items:
        group_key = item.get(key)
        if group_key not in result:
            result[group_key] = []
        result[group_key].append(item)
    return result


def sum_by_key(items: List[Dict], key: str, sum_key: str = "value") -> Dict[str, float]:
    """Sum values in list of dictionaries grouped by a key
    
    Args:
        items: List of dictionaries
        key: Key to group by
        sum_key: Key containing values to sum
        
    Returns:
        Dictionary with summed values
    """
    result = {}
    for item in items:
        group_key = item.get(key)
        value = item.get(sum_key, 0)
        result[group_key] = result.get(group_key, 0) + value
    return result


def filter_by_field(items: List[Dict], field: str, value: Any) -> List[Dict]:
    """Filter list of dictionaries by field value"""
    return [item for item in items if item.get(field) == value]


def sort_by_field(items: List[Dict], field: str, reverse: bool = False) -> List[Dict]:
    """Sort list of dictionaries by field"""
    return sorted(items, key=lambda x: x.get(field, ""), reverse=reverse)
