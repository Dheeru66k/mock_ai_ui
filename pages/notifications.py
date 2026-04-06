"""
Notifications Page
Display and manage notifications.
"""

import streamlit as st
from utils.helpers import format_timestamp, truncate_text


def render_notifications():
    """Render the notifications page"""
    
    st.markdown('<div class="section-header">🔔 Notifications</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Stay updated with important alerts and system notifications.</div>', unsafe_allow_html=True)
    
    data = st.session_state.get("mock_data", {})
    notifications = data.get("notifications", [])
    
    if not notifications:
        st.info("No notifications at this time.")
        return
    
    # Filter for unread/read
    tabs = st.tabs(["Unread", "All"])
    
    with tabs[0]:
        unread = [n for n in notifications if not n.get("read", True)]
        if not unread:
            st.info("All notifications marked as read!")
        else:
            for notif in unread:
                notif_class = f"notif-{notif['type']}"
                st.markdown(f"""
                <div class="{notif_class} notif-item">
                    <div style="font-weight:600;color:var(--text);">{notif['title']}</div>
                    <div style="color:var(--text2);font-size:0.85rem;margin-top:0.2rem;">{notif['msg']}</div>
                    <div style="color:var(--text2);font-size:0.75rem;margin-top:0.3rem;">{format_timestamp(notif['time'])}</div>
                </div>
                """, unsafe_allow_html=True)
    
    with tabs[1]:
        for notif in notifications:
            notif_class = f"notif-{notif['type']}"
            st.markdown(f"""
            <div class="{notif_class} notif-item">
                <div style="font-weight:600;color:var(--text);">{notif['title']}</div>
                <div style="color:var(--text2);font-size:0.85rem;margin-top:0.2rem;">{notif['msg']}</div>
                <div style="color:var(--text2);font-size:0.75rem;margin-top:0.3rem;">{format_timestamp(notif['time'])}</div>
            </div>
            """, unsafe_allow_html=True)
