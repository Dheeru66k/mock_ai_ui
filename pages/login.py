"""
Login Page
Azure AD SSO authentication interface.
"""

import streamlit as st
from components.styles import render_login_background
from components.logo import platform_logo_svg
from auth.azure_sso import get_sso_manager
from config.settings import validate_azure_sso


def render_login_page():
    """Render the login page with Azure SSO"""
    
    sso = get_sso_manager()
    sso.init_session()
    
    render_login_background()
    
    col_l, col_c, col_r = st.columns([1, 1.1, 1])
    
    with col_c:
        # Logo and title
        st.markdown(f"""
        <div style="text-align:center; margin-bottom: 2rem; margin-top: 3rem;">
            <div style="display:inline-flex;align-items:center;justify-content:center;
                        width:80px;height:80px;border-radius:22px;
                        background:linear-gradient(135deg,rgba(0,217,138,0.12),rgba(255,176,32,0.08));
                        border:1px solid rgba(0,217,138,0.25);
                        margin-bottom:1.2rem;box-shadow:0 0 40px rgba(0,217,138,0.12);">
                {platform_logo_svg(64)}
            </div>
            <div style="font-size:1.75rem;font-weight:800;color:var(--text);
                        letter-spacing:-0.03em;line-height:1.1;margin-bottom:0.35rem;">
                AI Platform <span style="color:var(--accent);">Hub</span>
            </div>
            <div style="font-size:0.85rem;color:var(--text2);font-weight:500;
                        letter-spacing:0.04em;text-transform:uppercase;">
                Enterprise Use Case Management
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Login card
        st.markdown("""
        <div style="background:var(--surface);border:1px solid var(--border);
                    border-radius:20px;padding:2.2rem 2.4rem;
                    box-shadow:0 8px 40px rgba(0,0,0,0.25);">
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="font-size:0.9rem;font-weight:700;color:var(--text);margin-bottom:1.2rem;text-align:center;">Sign in to your account</div>', unsafe_allow_html=True)
        
        # Check if Azure SSO is configured
        if not validate_azure_sso():
            st.warning("""
                ⚠️ Azure AD is not configured. 
                Please set the following environment variables:
                - AZURE_CLIENT_ID
                - AZURE_TENANT_ID  
                - AZURE_CLIENT_SECRET
                
                For now, using demo credentials.
            """)
            
            # Demo login fallback
            st.markdown('<div style="font-size:0.72rem;font-weight:700;color:var(--text2);letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.3rem;">Demo Email</div>', unsafe_allow_html=True)
            email = st.text_input(
                "Email",
                value="demo@company.com",
                placeholder="user@company.com",
                label_visibility="collapsed"
            )
            
            if st.button("Sign in with Demo Account →", use_container_width=True):
                # Create a demo user object
                demo_user = {
                    "displayName": "Demo User",
                    "mail": email,
                    "userPrincipalName": email,
                    "department": "General",
                }
                demo_token = {"access_token": "demo_token_placeholder"}
                sso.set_logged_in(demo_user, demo_token)
                st.rerun()
        else:
            # Production Azure AD login
            auth_url = sso.get_auth_url()
            
            st.markdown(f"""
            <div style="text-align: center;">
                <a href="{auth_url}" target="_self">
                    <button style="
                        width: 100%;
                        padding: 0.75rem;
                        background: linear-gradient(135deg, var(--accent), var(--accent2));
                        color: #070C0A;
                        border: none;
                        border-radius: 8px;
                        font-weight: 600;
                        font-size: 0.95rem;
                        cursor: pointer;
                        transition: transform 0.15s;
                    " onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                        🔐 Sign in with Microsoft →
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div style="text-align:center;font-size:0.78rem;color:var(--text2);margin-top:1rem;">Your organization uses Microsoft Azure AD for authentication.</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Footer
        st.markdown("""
        <div style="text-align:center;margin-top:1.5rem;font-size:0.75rem;color:var(--text2);">
            <p>Protected by enterprise-grade security</p>
            <p style="margin-top:0.5rem;">For support, contact: <code style="background:var(--surface2);padding:2px 6px;border-radius:4px;">support@company.com</code></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Theme toggle
        st.markdown("<br>", unsafe_allow_html=True)
        col_t1, col_t2, col_t3 = st.columns([1, 1, 1])
        with col_t2:
            if st.button(
                "🌙 Dark" if not st.session_state.get("dark_mode", True) else "☀️ Light",
                use_container_width=True,
                key="login_theme"
            ):
                st.session_state.dark_mode = not st.session_state.get("dark_mode", True)
                st.rerun()
