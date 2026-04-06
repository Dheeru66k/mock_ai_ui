"""
Sidebar Component
Navigation sidebar with user info and theme toggle.
"""

import streamlit as st
from components.logo import platform_logo_svg
from auth.azure_sso import get_sso_manager


def render_sidebar():
    """Render the main application sidebar with navigation"""
    
    sso = get_sso_manager()
    user = sso.get_current_user()
    
    if not user:
        return
    
    email = user.get("mail") or user.get("userPrincipalName", "Unknown")
    name = user.get("displayName", "User")
    department = user.get("department", "General")
    
    # Get user roles
    roles = sso.get_user_roles(email)
    
    with st.sidebar:
        # Platform logo at top
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:0.7rem;
                    padding:0.4rem 0 1.2rem 0;border-bottom:1px solid var(--border);margin-bottom:1rem;">
            <div style="width:34px;height:34px;border-radius:9px;flex-shrink:0;
                        background:linear-gradient(135deg,rgba(0,217,138,0.15),rgba(255,176,32,0.1));
                        border:1px solid rgba(0,217,138,0.3);
                        display:flex;align-items:center;justify-content:center;">
                {platform_logo_svg(26)}
            </div>
            <div>
                <div style="font-weight:800;font-size:0.9rem;color:var(--text);letter-spacing:-0.01em;">
                    AI Platform <span style="color:var(--accent);">Hub</span>
                </div>
                <div style="font-size:0.68rem;color:var(--text2);letter-spacing:0.05em;text-transform:uppercase;">Enterprise</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # User info card
        initials = (name.split()[0][0] + (name.split()[-1][0] if len(name.split()) > 1 else "?")).upper()
        
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:0.75rem;
                    background:var(--surface2);border:1px solid var(--border);
                    border-radius:12px;padding:0.7rem 0.9rem;margin-bottom:1.2rem;">
            <div style="width:34px;height:34px;border-radius:9px;flex-shrink:0;
                        background:linear-gradient(135deg,var(--accent),var(--accent2));
                        display:flex;align-items:center;justify-content:center;
                        font-weight:800;color:#070C0A;font-size:0.95rem;">
                {initials}
            </div>
            <div>
                <div style="font-weight:600;font-size:0.86rem;color:var(--text);">{name}</div>
                <div style="font-size:0.72rem;color:var(--text2);">{department}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation sections
        st.markdown('<div style="font-size:0.7rem;font-weight:600;color:var(--text2);letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.4rem;">Main</div>', unsafe_allow_html=True)
        
        def nav_btn(icon: str, label: str, page: str):
            """Create navigation button"""
            active = st.session_state.get("active_page") == page
            
            if st.button(
                f"{icon} {label}",
                key=f"nav_{page}",
                use_container_width=True,
                type="primary" if active else "secondary"
            ):
                st.session_state.active_page = page
                st.session_state.selected_uc = None
                st.rerun()
        
        nav_btn("📊", "Dashboard", "Dashboard")
        nav_btn("📦", "Use Cases", "Use Cases")
        
        # Analytics and cost tracking for AI team
        if "AI Team" in roles or "Admin" in roles:
            st.markdown('<div style="font-size:0.7rem;font-weight:600;color:var(--text2);letter-spacing:0.08em;text-transform:uppercase;margin:0.8rem 0 0.4rem 0;">Analytics</div>', unsafe_allow_html=True)
            nav_btn("📈", "Analytics", "Analytics")
            nav_btn("💰", "Cost Tracking", "Cost Tracking")
            nav_btn("⚡", "Performance", "Performance")
        
        st.markdown('<div style="font-size:0.7rem;font-weight:600;color:var(--text2);letter-spacing:0.08em;text-transform:uppercase;margin:0.8rem 0 0.4rem 0;">Management</div>', unsafe_allow_html=True)
        
        nav_btn("🤖", "Models", "Models")
        
        if "AI Team" in roles or "Admin" in roles:
            nav_btn("📋", "Activity Log", "Activity Log")
            nav_btn("👥", "User Feedback", "User Feedback")
        
        st.markdown('<div style="font-size:0.7rem;font-weight:600;color:var(--text2);letter-spacing:0.08em;text-transform:uppercase;margin:0.8rem 0 0.4rem 0;">System</div>', unsafe_allow_html=True)
        
        nav_btn("🔔", "Notifications", "Notifications")
        nav_btn("⚙️", "Settings", "Settings")
        
        if "Admin" in roles:
            nav_btn("🛡️", "Admin Panel", "Admin Panel")
        
        st.markdown("---")
        
        # Theme toggle and logout
        col1, col2 = st.columns(2)
        with col1:
            if st.button(
                "🌙 Dark" if not st.session_state.get("dark_mode", True) else "☀️ Light",
                use_container_width=True,
                key="theme_toggle"
            ):
                st.session_state.dark_mode = not st.session_state.get("dark_mode", True)
                st.rerun()
        
        with col2:
            if st.button("Sign Out", use_container_width=True, key="sign_out"):
                sso.logout()
                st.rerun()
