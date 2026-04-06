"""
Use Cases Page
Manage and monitor AI use cases.
"""

import streamlit as st
import pandas as pd
from components.logo import get_usecase_icon_svg
from utils.helpers import format_currency, format_number


def render_use_cases():
    """Render the use cases management page"""
    
    st.markdown('<div class="section-header">📦 Use Cases</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Manage and monitor all AI use cases across your organization.</div>', unsafe_allow_html=True)
    
    data = st.session_state.get("mock_data", {})
    use_cases = data.get("use_cases", [])
    
    # Filter options
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        status_filter = st.multiselect(
            "Status",
            options=["active", "draft", "inactive"],
            default=["active"],
            key="uc_status_filter"
        )
    
    with col2:
        dept_filter = st.multiselect(
            "Department",
            options=list(set(uc["business_unit"] for uc in use_cases)),
            key="uc_dept_filter"
        )
    
    with col3:
        type_filter = st.multiselect(
            "Type",
            options=list(set(uc["type"] for uc in use_cases)),
            key="uc_type_filter"
        )
    
    # Filter use cases
    filtered_ucs = use_cases
    if status_filter:
        filtered_ucs = [u for u in filtered_ucs if u["status"] in status_filter]
    if dept_filter:
        filtered_ucs = [u for u in filtered_ucs if u["business_unit"] in dept_filter]
    if type_filter:
        filtered_ucs = [u for u in filtered_ucs if u["type"] in type_filter]
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display use cases
    if not filtered_ucs:
        st.info("No use cases match your filters.")
        return
    
    for uc in filtered_ucs:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([0.5, 2, 1, 1, 1])
            
            with col1:
                st.markdown(f'<div style="font-size:32px;">{uc["type"][0]}</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="padding:0.5rem;">
                    <div style="font-weight:600;font-size:1.05rem;color:var(--text);">{uc['name']}</div>
                    <div style="font-size:0.8rem;color:var(--text2);margin-top:0.2rem;">{uc['description'][:80]}...</div>
                    <div style="font-size:0.75rem;color:var(--text2);margin-top:0.3rem;">Owner: {uc['owner_name']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                status_color = "#00D98A" if uc["status"] == "active" else "#FFB020"
                st.markdown(f'<div style="color:{status_color};font-weight:600;">{uc["status"].upper()}</div>', unsafe_allow_html=True)
            
            with col4:
                st.metric("Cost/mo", format_currency(uc["monthly_cost"]))
            
            with col5:
                st.metric("Calls/mo", format_number(uc["usage_count"]))
            
            st.divider()
