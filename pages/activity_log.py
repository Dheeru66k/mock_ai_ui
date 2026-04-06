"""
Activity Log Page
Audit trail of all system activities.
"""

import streamlit as st
import pandas as pd
from utils.helpers import format_timestamp


def render_activity_log():
    """Render the activity log page"""
    
    st.markdown('<div class="section-header">📋 Activity Log</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Audit trail of all platform activities and changes.</div>', unsafe_allow_html=True)
    
    data = st.session_state.get("mock_data", {})
    audit = data.get("audit", [])
    
    if not audit:
        st.info("No activity log available.")
        return
    
    # Filter options
    col1, col2 = st.columns(2)
    
    with col1:
        action_filter = st.selectbox(
            "Action Type",
            options=["All"] + list(set(a["action"] for a in audit)),
            key="action_filter"
        )
    
    with col2:
        days_filter = st.slider("Last N days", 1, 90, 30, key="days_filter")
    
    # Filter audit log
    filtered_audit = audit
    if action_filter != "All":
        filtered_audit = [a for a in filtered_audit if a["action"] == action_filter]
    
    # Create dataframe
    df_audit = pd.DataFrame([
        {
            "Time": format_timestamp(a["timestamp"]),
            "Actor": a["actor"],
            "Action": a["action"],
            "Detail": a["detail"],
            "Use Case": a["uc_id"],
        }
        for a in filtered_audit
    ])
    
    st.dataframe(df_audit, use_container_width=True, hide_index=True)
