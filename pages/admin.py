"""
Admin Panel
Administrative controls and system management.
"""

import streamlit as st
import pandas as pd


def render_admin():
    """Render the admin panel"""
    
    st.markdown('<div class="section-header">🛡️ Admin Panel</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">System administration and configuration.</div>', unsafe_allow_html=True)
    
    tabs = st.tabs(["Configuration", "Users", "System", "Documentation"])
    
    with tabs[0]:
        st.subheader("Platform Configuration")
        
        from config.settings import config, COLOR_SCHEME
        
        st.markdown("**Business Units (Departments)**")
        st.info("Add or remove departments in config/settings.py -> BUSINESS_UNITS")
        
        for dept in config.BUSINESS_UNITS:
            st.text(f"• {dept}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Feature Flags**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Enable Mock Data", value=config.ENABLE_MOCK_DATA, disabled=True)
            st.checkbox("Enable Analytics", value=config.ENABLE_ANALYTICS, disabled=True)
        with col2:
            st.checkbox("Enable Cost Tracking", value=config.ENABLE_COST_TRACKING, disabled=True)
            st.checkbox("Enable Performance Monitoring", value=config.ENABLE_PERFORMANCE_MONITORING, disabled=True)
    
    with tabs[1]:
        st.subheader("User Management")
        
        st.info("User management is handled through Azure Active Directory. Users are automatically provisioned.")
        
        st.markdown("""
        **User Roles**:
        - **User**: Basic access to own use cases
        - **Marketing/Finance/Operations**: Department-specific access
        - **AI Team**: Full access to analytics and cost tracking
        - **Admin**: Full system access
        
        Roles are assigned based on Azure AD group membership.
        """)
    
    with tabs[2]:
        st.subheader("System Information")
        
        from config.settings import config
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text(f"App Version: {config.APP_VERSION}")
            st.text(f"App Title: {config.APP_TITLE}")
        
        with col2:
            st.text(f"Layout: {config.LAYOUT}")
            st.text(f"Cache Timeout: {config.CACHE_TIMEOUT_SECONDS}s")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Environment Variables Status**")
        
        from config.settings import validate_azure_sso, api_keys
        
        if validate_azure_sso():
            st.success("✅ Azure AD configured")
        else:
            st.warning("⚠️ Azure AD not configured")
        
        if api_keys.OPENAI_API_KEY:
            st.success("✅ OpenAI configured")
        else:
            st.warning("⚠️ OpenAI not configured")
    
    with tabs[3]:
        st.subheader("Documentation Links")
        
        st.markdown("""
        - [README](../docs/README.md) - Main documentation
        - [Add Use Case Guide](../docs/ADD_USECASE_GUIDE.md) - How to add new use cases
        - [API Keys Guide](../docs/API_KEYS_GUIDE.md) - API key setup
        - [Deployment Guide](../docs/DEPLOYMENT_GUIDE.md) - Production deployment
        """)
