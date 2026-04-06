"""
CSS Styles and Theme Management
Centralized styling for the entire application.
"""

import streamlit as st
from config.settings import COLOR_SCHEME


def inject_global_css():
    """Inject all global CSS styles into the app"""
    dark = st.session_state.get("dark_mode", True)
    colors = COLOR_SCHEME["dark"] if dark else COLOR_SCHEME["light"]
    
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=Fira+Code:wght@400;500&display=swap');

    :root {{
        --bg: {colors['bg']};
        --surface: {colors['surface']};
        --surface2: {colors['surface2']};
        --border: {colors['border']};
        --text: {colors['text']};
        --text2: {colors['text2']};
        --accent: {colors['accent']};
        --accent2: {colors['accent2']};
        --green: {colors['green']};
        --red: {colors['red']};
        --orange: {colors['orange']};
        --card: {colors['card_bg']};
    }}

    * {{ font-family: 'Plus Jakarta Sans', sans-serif !important; }}
    code, pre, .stCode {{ font-family: 'Fira Code', monospace !important; }}

    .stApp {{ background: var(--bg) !important; color: var(--text) !important; }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: var(--surface) !important;
        border-right: 1px solid var(--border) !important;
    }}
    [data-testid="stSidebar"] * {{ color: var(--text) !important; }}

    /* Main content */
    .main .block-container {{ padding: 1.5rem 2rem; max-width: 1400px; }}

    /* Metric cards */
    .metric-card {{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 0.5rem;
        position: relative;
        overflow: hidden;
    }}
    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent), var(--accent2));
    }}
    .metric-label {{ color: var(--text2); font-size: 0.78rem; font-weight: 500; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 0.4rem; }}
    .metric-value {{ color: var(--text); font-size: 1.9rem; font-weight: 700; line-height: 1; }}
    .metric-delta {{ font-size: 0.78rem; margin-top: 0.3rem; }}
    .delta-up {{ color: var(--green); }}
    .delta-down {{ color: var(--red); }}

    /* Use case cards */
    .uc-card {{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.3rem 1.5rem;
        margin-bottom: 0.8rem;
        transition: border-color 0.2s, box-shadow 0.2s;
    }}
    .uc-card:hover {{
        border-color: var(--accent);
        box-shadow: 0 0 20px rgba(0,217,138,0.08);
    }}
    .uc-title {{ font-size: 1rem; font-weight: 700; color: var(--text); margin-bottom: 0.3rem; }}
    .uc-meta {{ font-size: 0.8rem; color: var(--text2); }}

    /* Status badges */
    .badge {{
        display: inline-block;
        padding: 0.18rem 0.65rem;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.04em;
    }}
    .badge-active  {{ background: rgba(0,217,138,0.12); color: var(--green); }}
    .badge-inactive{{ background: rgba(255,77,106,0.12); color: var(--red); }}
    .badge-draft   {{ background: rgba(255,176,32,0.12); color: var(--orange); }}
    .badge-pending {{ background: rgba(0,217,138,0.10); color: var(--accent); }}

    /* Section headers */
    .section-header {{
        font-size: 1.4rem;
        font-weight: 800;
        color: var(--text);
        margin-bottom: 0.2rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        letter-spacing: -0.02em;
    }}
    .section-sub {{
        color: var(--text2);
        font-size: 0.85rem;
        margin-bottom: 1.2rem;
    }}

    /* Notification items */
    .notif-item {{
        background: var(--surface2);
        border-left: 3px solid var(--accent);
        border-radius: 0 8px 8px 0;
        padding: 0.7rem 1rem;
        margin-bottom: 0.5rem;
        font-size: 0.85rem;
    }}
    .notif-warn    {{ border-left-color: var(--orange); }}
    .notif-error   {{ border-left-color: var(--red); }}
    .notif-success {{ border-left-color: var(--green); }}

    /* Timeline / activity log */
    .activity-item {{
        display: flex;
        gap: 1rem;
        padding: 0.6rem 0;
        border-bottom: 1px solid var(--border);
        font-size: 0.84rem;
    }}
    .activity-time {{ color: var(--text2); min-width: 120px; }}
    .activity-text {{ color: var(--text); }}

    /* Override Streamlit default metric */
    [data-testid="stMetric"] {{
        background: var(--card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 1rem 1.2rem !important;
    }}
    [data-testid="stMetricLabel"] {{ color: var(--text2) !important; font-size: 0.8rem !important; }}
    [data-testid="stMetricValue"] {{ color: var(--text) !important; font-weight: 700 !important; }}

    /* Plotly charts transparent bg */
    .js-plotly-plot .plotly .modebar {{ background: transparent !important; }}

    /* Buttons */
    .stButton > button {{
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.84rem !important;
        transition: all 0.15s !important;
        border: 1px solid var(--border) !important;
        background: var(--surface2) !important;
        color: var(--text) !important;
    }}
    .stButton > button:hover {{
        border-color: var(--accent) !important;
        color: var(--accent) !important;
        box-shadow: 0 0 12px rgba(0,217,138,0.12) !important;
    }}

    /* Primary button */
    .primary-btn .stButton > button {{
        background: var(--accent) !important;
        color: #070C0A !important;
        border-color: var(--accent) !important;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        background: var(--surface2) !important;
        border-radius: 10px !important;
        padding: 4px !important;
        gap: 2px !important;
        border: none !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.84rem !important;
        color: var(--text2) !important;
        padding: 0.45rem 1rem !important;
    }}
    .stTabs [aria-selected="true"] {{
        background: var(--surface) !important;
        color: var(--accent) !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.2) !important;
    }}
    .stTabs [data-baseweb="tab-panel"] {{ padding-top: 1.2rem !important; }}

    /* Select boxes, inputs */
    .stSelectbox > div > div,
    .stMultiSelect > div > div,
    .stTextInput > div > div,
    .stNumberInput > div > div,
    .stTextArea > div > div {{
        background: var(--surface2) !important;
        border-color: var(--border) !important;
        border-radius: 8px !important;
        color: var(--text) !important;
    }}

    /* Slider */
    .stSlider [data-testid="stSlider"] {{ color: var(--accent) !important; }}

    /* Expander */
    .streamlit-expanderHeader {{
        background: var(--surface2) !important;
        border-radius: 8px !important;
        color: var(--text) !important;
        font-weight: 600 !important;
    }}

    /* DataFrames */
    .stDataFrame {{ border-radius: 10px !important; overflow: hidden !important; }}
    [data-testid="stDataFrame"] th {{
        background: var(--surface2) !important;
        color: var(--text2) !important;
        font-size: 0.78rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }}

    /* Horizontal rule */
    hr {{ border-color: var(--border) !important; }}

    /* Info/warning/error boxes */
    .stAlert {{ border-radius: 10px !important; border: none !important; }}

    /* Progress bar */
    .stProgress > div > div {{
        background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
        border-radius: 4px !important;
    }}

    /* Scrollbar */
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 3px; }}

    /* Hide Streamlit branding */
    #MainMenu, footer, header {{ visibility: hidden; }}

    /* Sidebar nav items */
    .nav-item {{
        padding: 0.55rem 0.8rem;
        border-radius: 8px;
        margin-bottom: 2px;
        cursor: pointer;
        font-size: 0.86rem;
        font-weight: 500;
        color: var(--text2);
        display: flex;
        align-items: center;
        gap: 0.6rem;
        transition: all 0.15s;
    }}
    .nav-item:hover, .nav-item.active {{
        background: rgba(0,217,138,0.1);
        color: var(--accent);
    }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


def render_login_background():
    """Render decorative background for login page"""
    st.markdown("""
    <style>
    .login-bg {{
        position: fixed; inset: 0; pointer-events: none; z-index: 0;
        overflow: hidden;
    }}
    .login-bg::before {{
        content: '';
        position: absolute;
        top: -200px; left: 50%; transform: translateX(-50%);
        width: 700px; height: 700px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(0,217,138,0.06) 0%, transparent 70%);
    }}
    .login-bg::after {{
        content: '';
        position: absolute;
        bottom: -150px; right: -100px;
        width: 500px; height: 500px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(255,176,32,0.05) 0%, transparent 70%);
    }}
    </style>
    <div class="login-bg"></div>
    """, unsafe_allow_html=True)
