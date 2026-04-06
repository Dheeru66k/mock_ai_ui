"""
Performance Monitoring Page
Monitor response times, success rates, and errors.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.charts import style_figure


def render_performance():
    """Render the performance monitoring page"""
    
    st.markdown('<div class="section-header">⚡ Performance Monitoring</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Track response times, success rates, and system health.</div>', unsafe_allow_html=True)
    
    data = st.session_state.get("mock_data", {})
    use_cases = data.get("use_cases", [])
    
    if not use_cases:
        st.info("No performance data available.")
        return
    
    tabs = st.tabs(["Response Times", "Success Rates", "Error Analysis"])
    
    with tabs[0]:
        st.subheader("Average Response Times")
        
        df_resp = pd.DataFrame({
            "Use Case": [uc["name"] for uc in use_cases],
            "Response Time (ms)": [uc["avg_response_ms"] for uc in use_cases],
        }).sort_values("Response Time (ms)")
        
        fig = px.barh(df_resp, x="Response Time (ms)", y="Use Case",
                     title="Average Response Time by Use Case")
        fig = style_figure(fig, 350)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    
    with tabs[1]:
        st.subheader("Success Rates")
        
        df_success = pd.DataFrame({
            "Use Case": [uc["name"] for uc in use_cases],
            "Success Rate (%)": [uc["success_rate"] for uc in use_cases],
        }).sort_values("Success Rate (%)")
        
        fig = px.bar(df_success, x="Use Case", y="Success Rate (%)",
                    color="Success Rate (%)",
                    color_continuous_scale=["#E74C3C", "#FFB020", "#00D98A"],
                    range_color=[90, 100],
                    title="Success Rate by Use Case")
        fig.update_xaxes(tickangle=-45)
        fig = style_figure(fig, 350)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    
    with tabs[2]:
        st.subheader("Error Distribution")
        
        st.markdown("**Common Error Types (Last 30 Days)**")
        
        error_types = {
            "Rate Limit": 28,
            "Timeout": 12,
            "Invalid Format": 8,
            "Content Filter": 5,
            "Context Overflow": 3,
            "Other": 4,
        }
        
        df_errors = pd.DataFrame({
            "Error Type": list(error_types.keys()),
            "Count": list(error_types.values())
        })
        
        fig = px.pie(df_errors, names="Error Type", values="Count",
                    title="Error Distribution",
                    color_discrete_sequence=["#E74C3C", "#F39C12", "#00D98A", "#FFB020", "#34D399", "#60A5FA"])
        fig = style_figure(fig, 350)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
