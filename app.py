"""
AI Use Case Management Platform - Main Router
A modular Streamlit application for managing AI use cases.
Production-ready with Azure SSO, role-based access, and comprehensive analytics.

Module Structure:
- config/ : Configuration and environment variables
- auth/   : Azure SSO authentication
- pages/  : Individual page components (11 pages)
- components/ : Reusable UI components
- utils/  : Helper functions and utilities
- data/   : Data models and mock data generation
"""

import streamlit as st
from config.settings import config, get_config, get_azure_sso
from auth.azure_sso import AzureSSOManager
from components.styles import inject_global_css
from components.sidebar import render_sidebar
from data.mock_data import generate_all_mock_data

# Import all page modules
from pages.login import render_login
from pages.dashboard import render_dashboard
from pages.use_cases import render_use_cases
from pages.models import render_models
from pages.analytics import render_analytics
from pages.cost_tracking import render_cost_tracking
from pages.performance import render_performance
from pages.notifications import render_notifications
from pages.settings import render_settings
from pages.activity_log import render_activity_log
from pages.user_feedback import render_user_feedback
from pages.admin import render_admin


def init_app():
    """Initialize application settings and session state"""
    # Configure page
    st.set_page_config(
        page_title=config.APP_TITLE,
        page_icon=config.APP_ICON,
        layout=config.LAYOUT,
        initial_sidebar_state=config.SIDEBAR_STATE,
    )
    
    # Inject global CSS styles
    inject_global_css()
    
    # Initialize session state
    if "auth_manager" not in st.session_state:
        st.session_state.auth_manager = AzureSSOManager()
        st.session_state.auth_manager.init_session()
    
    # Initialize active page
    if "active_page" not in st.session_state:
        st.session_state.active_page = "login" if not st.session_state.auth_manager.is_authenticated() else "dashboard"
    
    # Initialize dark mode
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = config.DARK_MODE_DEFAULT
    
    # Generate and cache mock data
    if "mock_data" not in st.session_state and config.ENABLE_MOCK_DATA:
        st.session_state.mock_data = generate_all_mock_data()


def main():
    """Main application router"""
    init_app()
    
    # Authentication check
    auth_manager = st.session_state.auth_manager
    is_authenticated = auth_manager.is_authenticated()
    
    # Show login page if not authenticated
    if not is_authenticated:
        render_login()
        return
    
    # Render sidebar with user info and navigation
    render_sidebar()
    
    # Route to appropriate page based on active_page state
    page = st.session_state.get("active_page", "dashboard")
    
    # Define page access control (role-based)
    restricted_pages = {
        "analytics": ["AI Team", "Admin"],
        "cost_tracking": ["AI Team", "Admin"],
        "performance": ["AI Team", "Admin"],
        "admin": ["Admin"],
    }
    
    # Check access permissions
    user_roles = auth_manager.get_user_roles(auth_manager.session_state.get("user_email", ""))
    if page in restricted_pages:
        if not any(role in user_roles for role in restricted_pages[page]):
            st.warning("⛔ You don't have access to this page. Please contact your administrator.")
            st.session_state.active_page = "dashboard"
            st.rerun()
    
    # Route to page
    page_routes = {
        "dashboard": render_dashboard,
        "use_cases": render_use_cases,
        "models": render_models,
        "analytics": render_analytics,
        "cost_tracking": render_cost_tracking,
        "performance": render_performance,
        "notifications": render_notifications,
        "settings": render_settings,
        "activity_log": render_activity_log,
        "user_feedback": render_user_feedback,
        "admin": render_admin,
    }
    
    if page in page_routes:
        page_routes[page]()
    else:
        st.error(f"Page '{page}' not found")
        st.session_state.active_page = "dashboard"
        st.rerun()


if __name__ == "__main__":
    main()
