"""
Dashboard Page
Main overview page with key metrics and use case summary.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.helpers import generate_metric_card_html, format_currency, format_number
from utils.charts import style_figure, get_chart_theme


def render_dashboard():
    """Render the dashboard page"""
    
    st.markdown('<div class="section-header">📊 Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Overview of all AI use cases, costs, and performance metrics.</div>', unsafe_allow_html=True)
    
    data = st.session_state.get("mock_data", {})
    use_cases = data.get("use_cases", [])
    
    if not use_cases:
        st.info("No use cases available. Start by creating a new use case!")
        return
    
    # Key metrics
    total_usage = sum(uc["usage_count"] for uc in use_cases)
    total_cost = sum(uc["monthly_cost"] for uc in use_cases)
    active_count = sum(1 for uc in use_cases if uc["status"] == "active")
    avg_success = np.mean([uc["success_rate"] for uc in use_cases])
    
    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1:
        st.markdown(
            generate_metric_card_html(
                "Active Use Cases",
                str(active_count),
                f"{active_count}/{len(use_cases)} total"
            ),
            unsafe_allow_html=True
        )
    with mc2:
        st.markdown(
            generate_metric_card_html(
                "Monthly Cost (MTD)",
                format_currency(total_cost),
                "8.1% vs last month",
                False
            ),
            unsafe_allow_html=True
        )
    with mc3:
        st.markdown(
            generate_metric_card_html(
                "Total API Calls",
                format_number(total_usage),
                "+12% vs last month"
            ),
            unsafe_allow_html=True
        )
    with mc4:
        st.markdown(
            generate_metric_card_html(
                "Success Rate",
                f"{avg_success:.1f}%",
                "Platform average"
            ),
            unsafe_allow_html=True
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs for different views
    tabs = st.tabs(["All Use Cases", "By Department", "Cost Analysis"])
    
    with tabs[0]:
        st.subheader("All Active Use Cases")
        
        # Display use cases as cards
        for uc in use_cases:
            if uc["status"] != "active":
                continue
            
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div style="padding:0.5rem;border-bottom:1px solid var(--border);">
                    <div style="font-weight:600;font-size:1rem;color:var(--text);">{uc['name']}</div>
                    <div style="font-size:0.8rem;color:var(--text2);margin-top:0.2rem;">{uc['business_unit']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.metric("Calls/Month", format_number(uc["usage_count"]))
            
            with col3:
                st.metric("Cost/Month", format_currency(uc["monthly_cost"]))
            
            with col4:
                st.metric("Success Rate", f"{uc['success_rate']:.1f}%")
    
    with tabs[1]:
        # Group by department
        st.subheader("Cost by Department")
        
        dept_data = {}
        for uc in use_cases:
            dept = uc["business_unit"]
            dept_data[dept] = dept_data.get(dept, 0) + uc["monthly_cost"]
        
        df_dept = pd.DataFrame({
            "Department": list(dept_data.keys()),
            "Cost ($)": list(dept_data.values())
        })
        
        fig = px.pie(
            df_dept,
            names="Department",
            values="Cost ($)",
            title="Cost Distribution by Department",
            color_discrete_sequence=["#00D98A", "#FFB020", "#34D399", "#60A5FA"]
        )
        fig = style_figure(fig, 350)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    
    with tabs[2]:
        st.subheader("Cost Breakdown")
        
        df_chart = pd.DataFrame({
            "Use Case": [uc["name"][:30] for uc in use_cases],
            "Cost": [uc["monthly_cost"] for uc in use_cases],
            "Department": [uc["business_unit"] for uc in use_cases],
        }).sort_values("Cost", ascending=False)
        
        fig = px.bar(
            df_chart,
            x="Use Case",
            y="Cost",
            color="Department",
            title="Monthly Cost by Use Case",
            color_discrete_sequence=["#00D98A", "#FFB020", "#34D399"]
        )
        fig.update_layout(xaxis_tickangle=-45)
        fig = style_figure(fig, 350)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
