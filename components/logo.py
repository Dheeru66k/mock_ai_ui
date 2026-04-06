"""
Logo and Icon Components
SVG logos and icons for use throughout the application.
"""

from utils.helpers import svg_to_img


def platform_logo_svg(size: int = 72) -> str:
    """Generate platform logo SVG as HTML img tag
    
    Args:
        size: Logo size in pixels
        
    Returns:
        HTML img tag with base64 encoded SVG
    """
    a, g = "#00D98A", "#FFB020"  # accent colors
    
    svg = f"""<svg width="72" height="72" viewBox="0 0 72 72" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="pg" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{a}" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="{a}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <circle cx="36" cy="36" r="32" fill="url(#pg)"/>
  <polygon points="36,6 62,21 62,51 36,66 10,51 10,21"
           fill="none" stroke="{a}" stroke-width="1.5" stroke-opacity="0.5"/>
  <polygon points="36,14 56,25.5 56,47.5 36,58 16,47.5 16,25.5"
           fill="none" stroke="{g}" stroke-width="1" stroke-opacity="0.4"
           transform="rotate(30 36 36)"/>
  <circle cx="36" cy="6"  r="2.8" fill="{g}" opacity="0.9"/>
  <circle cx="62" cy="21" r="2.8" fill="{g}" opacity="0.9"/>
  <circle cx="62" cy="51" r="2.8" fill="{g}" opacity="0.9"/>
  <circle cx="36" cy="66" r="2.8" fill="{g}" opacity="0.9"/>
  <circle cx="10" cy="51" r="2.8" fill="{g}" opacity="0.9"/>
  <circle cx="10" cy="21" r="2.8" fill="{g}" opacity="0.9"/>
  <line x1="36" y1="9"  x2="36" y2="26" stroke="{a}" stroke-width="1.2" stroke-opacity="0.45"/>
  <line x1="59" y1="23" x2="44" y2="31" stroke="{a}" stroke-width="1.2" stroke-opacity="0.45"/>
  <line x1="59" y1="49" x2="44" y2="41" stroke="{a}" stroke-width="1.2" stroke-opacity="0.45"/>
  <line x1="36" y1="63" x2="36" y2="46" stroke="{a}" stroke-width="1.2" stroke-opacity="0.45"/>
  <line x1="13" y1="49" x2="28" y2="41" stroke="{a}" stroke-width="1.2" stroke-opacity="0.45"/>
  <line x1="13" y1="23" x2="28" y2="31" stroke="{a}" stroke-width="1.2" stroke-opacity="0.45"/>
  <polygon points="36,26 44,31 44,41 36,46 28,41 28,31"
           fill="{a}" fill-opacity="0.1" stroke="{a}" stroke-width="1.5"/>
  <circle cx="36" cy="36" r="7"   fill="{a}" fill-opacity="0.18" stroke="{a}" stroke-width="2"/>
  <circle cx="36" cy="36" r="3.2" fill="{a}"/>
  <text x="36" y="40.5" text-anchor="middle" font-size="5.5" font-weight="800"
        fill="{a}" font-family="monospace" letter-spacing="1.5">AI</text>
</svg>"""
    
    return svg_to_img(svg, size)


def get_usecase_icon_svg(usecase_type: str, size: int = 44) -> str:
    """Get icon SVG for a specific use case type
    
    Args:
        usecase_type: The type of use case (e.g., "Content Generation")
        size: Icon size in pixels
        
    Returns:
        HTML img tag with base64 encoded SVG
    """
    import streamlit as st
    
    dark = st.session_state.get("dark_mode", True)
    a = "#00D98A" if dark else "#00A86B"   # accent
    g = "#FFB020" if dark else "#D4890A"   # accent2
    
    icons = {
        "Content Generation": f"""
          <polygon points="10,34 14,22 28,10 36,18 22,34" fill="none" stroke="{a}" stroke-width="2" stroke-linejoin="round"/>
          <line x1="24" y1="14" x2="32" y2="22" stroke="{a}" stroke-width="2"/>
          <line x1="7"  y1="34" x2="4"  y2="38" stroke="{g}" stroke-width="2.5" stroke-linecap="round"/>
          <line x1="4"  y1="36" x2="9"  y2="38" stroke="{g}" stroke-width="2.5" stroke-linecap="round"/>
          <line x1="18" y1="38" x2="38" y2="38" stroke="{a}" stroke-width="1.5" stroke-linecap="round" opacity="0.4"/>
          <line x1="18" y1="42" x2="30" y2="42" stroke="{a}" stroke-width="1.5" stroke-linecap="round" opacity="0.4"/>""",
        
        "Text Analysis": f"""
          <circle cx="19" cy="19" r="11" fill="none" stroke="{a}" stroke-width="2.2"/>
          <line x1="27" y1="27" x2="39" y2="39" stroke="{a}" stroke-width="2.8" stroke-linecap="round"/>
          <line x1="13" y1="16" x2="25" y2="16" stroke="{g}" stroke-width="1.8" stroke-linecap="round" opacity="0.8"/>
          <line x1="13" y1="20" x2="22" y2="20" stroke="{g}" stroke-width="1.8" stroke-linecap="round" opacity="0.8"/>
          <line x1="13" y1="24" x2="19" y2="24" stroke="{g}" stroke-width="1.8" stroke-linecap="round" opacity="0.5"/>""",
        
        "Summarization": f"""
          <path d="M6,8 H38 L28,22 L28,36 L16,36 L16,22 Z" fill="{a}" fill-opacity="0.1"
                stroke="{a}" stroke-width="2" stroke-linejoin="round"/>
          <line x1="10" y1="8" x2="10" y2="4" stroke="{g}" stroke-width="2" stroke-linecap="round" opacity="0.6"/>
          <line x1="22" y1="8" x2="22" y2="4" stroke="{g}" stroke-width="2" stroke-linecap="round" opacity="0.6"/>
          <line x1="34" y1="8" x2="34" y2="4" stroke="{g}" stroke-width="2" stroke-linecap="round" opacity="0.6"/>
          <circle cx="22" cy="32" r="2.5" fill="{g}"/>""",
        
        "Document Review": f"""
          <path d="M8,4 H28 L38,14 V42 H8 Z" fill="{a}" fill-opacity="0.08"
                stroke="{a}" stroke-width="2" stroke-linejoin="round"/>
          <path d="M28,4 V14 H38" fill="none" stroke="{a}" stroke-width="2"/>
          <path d="M14,26 L19,31 L30,22" stroke="{g}" stroke-width="2.8" fill="none"
                stroke-linecap="round" stroke-linejoin="round"/>""",
        
        "Data Analysis": f"""
          <rect x="5"  y="26" width="9"  height="16" rx="1.5" fill="{a}" opacity="0.55"/>
          <rect x="18" y="16" width="9"  height="26" rx="1.5" fill="{a}"/>
          <rect x="31" y="8"  width="9"  height="34" rx="1.5" fill="{g}"/>
          <line x1="3" y1="43" x2="42"  y2="43" stroke="{a}" stroke-width="1.5" stroke-linecap="round"/>""",
        
        "Report Generation": f"""
          <polyline points="5,32 13,20 22,25 31,12 39,17"
                    fill="none" stroke="{a}" stroke-width="2.5"
                    stroke-linecap="round" stroke-linejoin="round"/>
          <circle cx="5"  cy="32" r="3" fill="{g}"/>
          <circle cx="13" cy="20" r="3" fill="{g}"/>
          <circle cx="22" cy="25" r="3" fill="{g}"/>
          <circle cx="31" cy="12" r="3" fill="{g}"/>
          <circle cx="39" cy="17" r="3" fill="{g}"/>
          <line x1="3" y1="38" x2="41" y2="38" stroke="{a}" stroke-width="1.2" opacity="0.35"/>""",
        
        "Anomaly Detection": f"""
          <path d="M22,4 L38,12 V24 C38,33 22,40 22,40 C22,40 6,33 6,24 V12 Z"
                fill="{a}" fill-opacity="0.08" stroke="{a}" stroke-width="2" stroke-linejoin="round"/>
          <polyline points="10,26 15,18 20,24 25,12 30,26"
                    fill="none" stroke="{g}" stroke-width="2.5"
                    stroke-linecap="round" stroke-linejoin="round"/>""",
        
        "Other": f"""
          <path d="M22,4 L24,16 L36,14 L27,22 L31,34 L22,27 L13,34 L17,22 L8,14 L20,16 Z"
                fill="{a}" fill-opacity="0.15" stroke="{a}"
                stroke-width="2" stroke-linejoin="round"/>
          <circle cx="22" cy="22" r="3" fill="{g}"/>""",
    }
    
    inner = icons.get(usecase_type, icons["Other"])
    svg = f"""<svg width="44" height="44" viewBox="0 0 44 44" xmlns="http://www.w3.org/2000/svg">{inner}</svg>"""
    return svg_to_img(svg, size)
