"""
Analytics Page
Detailed analytics and insights about use cases.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils.charts import style_figure


def render_analytics():
    """Render the analytics page"""
    
    st.markdown('<div class="section-header">📈 Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Detailed insights into use case performance and utilization.</div>', unsafe_allow_html=True)
    
    data = st.session_state.get("mock_data", {})
    use_cases = data.get("use_cases", [])
    dates = data.get("dates", [])
    usage_series = data.get("usage_series", {})
    
    if not use_cases:
        st.info("No data available.")
        return
    
    tabs = st.tabs(["Usage Trends", "Performance", "Model Comparison"])
    
    with tabs[0]:
        st.subheader("Usage Over Time")
        
        # Get last 30 days
        selected_uc = st.selectbox(
            "Select Use Case",
            options=[uc["name"] for uc in use_cases],
            key="analytics_uc"
        )
        
        selected_uc_id = next(u["id"] for u in use_cases if u["name"] == selected_uc)
        
        if selected_uc_id in usage_series:
            usage_data = usage_series[selected_uc_id][-30:]
            chart_dates = dates[-30:]
            
            df = pd.DataFrame({
                "Date": chart_dates,
                "Calls": usage_data
            })
            
            fig = px.line(
                df,
                x="Date",
                y="Calls",
                title=f"30-Day Usage - {selected_uc}",
                markers=True
            )
            fig = style_figure(fig, 350)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    
    with tabs[1]:
        st.subheader("Performance Metrics")
        
        metrics_df = pd.DataFrame([
            {
                "Use Case": uc["name"],
                "Avg Response (ms)": uc["avg_response_ms"],
                "Success Rate (%)": uc["success_rate"],
                "Monthly Cost": uc["monthly_cost"],
            }
            for uc in use_cases
        ])
        
        st.dataframe(metrics_df, use_container_width=True, hide_index=True)
    
    with tabs[2]:
        st.subheader("Model Usage")
        
        model_counts = {}
        for uc in use_cases:
            model = uc["model"]
            model_counts[model] = model_counts.get(model, 0) + 1
        
        df_models = pd.DataFrame({
            "Model": list(model_counts.keys()),
            "Use Cases": list(model_counts.values())
        })
        
        fig = px.pie(
            df_models,
            names="Model",
            values="Use Cases",
            title="Use Cases by Model"
        )
        fig = style_figure(fig, 350)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
