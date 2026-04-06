"""
User Feedback Page
View and analyze user feedback.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.helpers import format_timestamp
from utils.charts import style_figure


def render_feedback():
    """Render the user feedback page"""
    
    st.markdown('<div class="section-header">👥 User Feedback</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Insights from users about their experience with use cases.</div>', unsafe_allow_html=True)
    
    data = st.session_state.get("mock_data", {})
    feedback = data.get("feedback", [])
    
    if not feedback:
        st.info("No feedback available yet.")
        return
    
    tabs = st.tabs(["Overview", "By Use Case", "All Feedback"])
    
    with tabs[0]:
        st.subheader("Feedback Summary")
        
        # Summary stats
        avg_rating = pd.Series([f["rating"] for f in feedback]).mean()
        total_feedback = len(feedback)
        positive = sum(1 for f in feedback if f.get("rating", 0) >= 4)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Rating", f"{avg_rating:.1f}/5")
        with col2:
            st.metric("Total Feedback", total_feedback)
        with col3:
            st.metric("Positive %", f"{(positive/total_feedback*100):.0f}%")
        
        # Rating distribution
        ratings = pd.Series([f["rating"] for f in feedback])
        rating_counts = ratings.value_counts().sort_index()
        
        df_ratings = pd.DataFrame({
            "Rating": rating_counts.index,
            "Count": rating_counts.values
        })
        
        fig = px.bar(df_ratings, x="Rating", y="Count",
                    title="Feedback Rating Distribution",
                    color="Count",
                    color_continuous_scale=["#E74C3C", "#FFB020", "#00D98A"])
        fig = style_figure(fig, 300)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    
    with tabs[1]:
        st.subheader("Feedback by Use Case")
        
        df_uc_feedback = pd.DataFrame([
            {
                "Use Case": f["uc_name"],
                "Avg Rating": f["rating"],
            }
            for f in feedback
        ]).groupby("Use Case")["Avg Rating"].mean().reset_index().sort_values("Avg Rating", ascending=False)
        
        fig = px.bar(df_uc_feedback, x="Use Case", y="Avg Rating",
                    title="Average Rating by Use Case",
                    color="Avg Rating",
                    color_continuous_scale=["#E74C3C", "#FFB020", "#00D98A"],
                    range_color=[3, 5])
        fig.update_xaxes(tickangle=-45)
        fig = style_figure(fig, 350)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    
    with tabs[2]:
        st.subheader("All Feedback")
        
        for fb in feedback:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"""
                    **{fb['uc_name']}** (⭐ {fb['rating']}/5)
                    
                    {fb['comment']}
                    
                    By {fb['user_email']} • {format_timestamp(fb['time'])}
                    """)
                
                st.divider()
