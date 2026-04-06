"""
Cost Tracking Page
Monitor and analyze costs across use cases.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from utils.helpers import format_currency
from utils.charts import style_figure


def render_cost_tracking():
    """Render the cost tracking page"""
    
    st.markdown('<div class="section-header">💰 Cost Tracking</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Monitor and forecast AI spending across your organization.</div>', unsafe_allow_html=True)
    
    data = st.session_state.get("mock_data", {})
    use_cases = data.get("use_cases", [])
    dates = data.get("dates", [])
    cost_series = data.get("cost_series", {})
    
    if not use_cases:
        st.info("No cost data available.")
        return
    
    # Summary metrics
    total_cost = sum(uc["monthly_cost"] for uc in use_cases)
    budget_limit = 2000.0
    budget_pct = (total_cost / budget_limit) * 100
    
    mc1, mc2, mc3, mc4 = st.columns(4)
    
    with mc1:
        st.metric("Monthly Spend", format_currency(total_cost))
    with mc2:
        st.metric("Budget Limit", format_currency(budget_limit))
    with mc3:
        st.metric("Remaining", format_currency(budget_limit - total_cost))
    with mc4:
        st.metric("Usage %", f"{budget_pct:.1f}%")
    
    st.progress(min(budget_pct / 100, 1.0), text=f"{budget_pct:.1f}% of budget")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    tabs = st.tabs(["By Use Case", "By Department", "By Model", "Cost Trend"])
    
    with tabs[0]:
        st.subheader("Cost by Use Case")
        
        df_uc = pd.DataFrame({
            "Use Case": [uc["name"] for uc in use_cases],
            "Cost": [uc["monthly_cost"] for uc in use_cases],
            "Calls": [uc["usage_count"] for uc in use_cases],
        }).sort_values("Cost", ascending=False)
        
        df_uc["Cost/Call"] = df_uc["Cost"] / df_uc["Calls"]
        
        fig = px.bar(df_uc, x="Use Case", y="Cost", color="Cost", 
                    color_continuous_scale=["#FFB020", "#E74C3C"],
                    title="Monthly Cost by Use Case")
        fig.update_xaxes(tickangle=-45)
        fig = style_figure(fig, 350)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        
        st.dataframe(df_uc, use_container_width=True, hide_index=True)
    
    with tabs[1]:
        st.subheader("Cost by Department")
        
        dept_costs = {}
        for uc in use_cases:
            dept = uc["business_unit"]
            dept_costs[dept] = dept_costs.get(dept, 0) + uc["monthly_cost"]
        
        df_dept = pd.DataFrame({
            "Department": list(dept_costs.keys()),
            "Cost": list(dept_costs.values())
        })
        
        fig = px.pie(df_dept, names="Department", values="Cost",
                    title="Cost Distribution by Department")
        fig = style_figure(fig, 350)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    
    with tabs[2]:
        st.subheader("Cost by Model")
        
        model_costs = {}
        for uc in use_cases:
            model = uc["model"]
            model_costs[model] = model_costs.get(model, 0) + uc["monthly_cost"]
        
        df_model = pd.DataFrame({
            "Model": list(model_costs.keys()),
            "Cost": list(model_costs.values())
        }).sort_values("Cost", ascending=False)
        
        fig = px.bar(df_model, x="Model", y="Cost",
                    title="Monthly Cost by Model")
        fig = style_figure(fig, 350)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    
    with tabs[3]:
        st.subheader("Cost Trend Analysis")
        
        # Calculate daily costs
        daily_costs = np.zeros(len(dates))
        for uc_id, costs in cost_series.items():
            daily_costs += np.array(costs)
        
        cumulative = np.cumsum(daily_costs)
        
        df_trend = pd.DataFrame({
            "Date": dates,
            "Daily": daily_costs,
            "Cumulative": cumulative
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_trend["Date"], y=df_trend["Daily"],
                            name="Daily Cost", marker_color="rgba(0,217,138,0.5)"))
        fig.add_trace(go.Scatter(x=df_trend["Date"], y=df_trend["Cumulative"],
                                name="Cumulative", line=dict(color="#FFB020")))
        
        fig = style_figure(fig, 350)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
