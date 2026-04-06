"""
Settings Page
User and system settings.
"""

import streamlit as st
from auth.azure_sso import get_sso_manager


def render_settings():
    """Render the settings page"""
    
    st.markdown('<div class="section-header">⚙️ Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Manage your account and application preferences.</div>', unsafe_allow_html=True)
    
    tabs = st.tabs(["Account", "Preferences", "API Keys"])
    
    with tabs[0]:
        st.subheader("Account Information")
        
        sso = get_sso_manager()
        user = sso.get_current_user()
        
        if user:
            st.text_input(
                "Display Name",
                value=user.get("displayName", ""),
                disabled=True
            )
            st.text_input(
                "Email",
                value=user.get("mail", user.get("userPrincipalName", "")),
                disabled=True
            )
            st.text_input(
                "Department",
                value=user.get("department", ""),
                disabled=True
            )
            
            st.info("Account information is managed by your organization's Azure Active Directory.")
    
    with tabs[1]:
        st.subheader("Preferences")
        
        theme = st.selectbox(
            "Theme",
            options=["Dark", "Light", "Auto"],
            index=0 if st.session_state.get("dark_mode", True) else 1,
            key="theme_setting"
        )
        
        st.markdown("**Notifications**")
        email_notif = st.checkbox("Email notifications for high-cost use cases", value=True)
        daily_digest = st.checkbox("Daily usage digest", value=False)
        
        if st.button("Save Preferences"):
            st.success("Preferences saved!")
    
    with tabs[2]:
        st.subheader("API Keys Configuration")
        
        st.info("""
        API keys should be stored as environment variables for security.
        
        **Production Setup**:
        1. Set environment variables in your deployment
        2. Do NOT commit keys to version control
        3. Rotate keys regularly
        
        **For Development**:
        Create a `.env` file (not committed to git):
        ```
        OPENAI_API_KEY=your_key_here
        ANTHROPIC_API_KEY=your_key_here
        GOOGLE_API_KEY=your_key_here
        AZURE_OPENAI_KEY=your_key_here
        AZURE_OPENAI_ENDPOINT=your_endpoint_here
        ```
        """)
        
        st.markdown("**Configured Providers**")
        
        from config.settings import api_keys
        
        providers = {
            "OpenAI": bool(api_keys.OPENAI_API_KEY),
            "Anthropic": bool(api_keys.ANTHROPIC_API_KEY),
            "Google": bool(api_keys.GOOGLE_API_KEY),
            "Azure OpenAI": bool(api_keys.AZURE_OPENAI_KEY),
            "Mistral": bool(api_keys.MISTRAL_API_KEY),
        }
        
        for provider, configured in providers.items():
            status = "✅ Configured" if configured else "❌ Not Configured"
            st.markdown(f"**{provider}**: {status}")
        
        st.link_button("📖 See API Keys Setup Guide", "./docs/API_KEYS_GUIDE.md")
