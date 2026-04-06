"""
Models Page
Display and manage available LLM models.
"""

import streamlit as st
import pandas as pd
from data.models import AVAILABLE_MODELS
from utils.helpers import format_currency


def render_models():
    """Render the models page"""
    
    st.markdown('<div class="section-header">🤖 Available Models</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">View details about all available language models and their capabilities.</div>', unsafe_allow_html=True)
    
    # Convert models to dataframe
    model_data = []
    for model in AVAILABLE_MODELS:
        model_data.append({
            "Model": model.name,
            "Provider": model.provider,
            "Status": model.status.upper(),
            "Context": model.context_window,
            "Cost/1K Input": f"${model.cost_per_1k_input:.4f}",
            "Cost/1K Output": f"${model.cost_per_1k_output:.4f}",
            "Capabilities": ", ".join(model.capabilities),
        })
    
    df = pd.DataFrame(model_data)
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Model Pricing Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Most Cost-Effective**")
        cheapest = min(AVAILABLE_MODELS, key=lambda x: x.cost_per_1k_input + x.cost_per_1k_output)
        st.info(f"{cheapest.name} - ${cheapest.cost_per_1k_input + cheapest.cost_per_1k_output:.4f} per 1K tokens")
    
    with col2:
        st.markdown("**Largest Context Window**")
        largest_ctx = max(AVAILABLE_MODELS, key=lambda x: int(x.context_window.replace("K", "").replace("M", "000")))
        st.info(f"{largest_ctx.name} - {largest_ctx.context_window} token context")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("How to Use Models in Your Use Cases")
    
    st.markdown("""
    When creating a new use case or updating an existing one:
    
    1. **Select the Right Model**: Choose based on your specific needs:
       - **Cost**: Use gpt-4o-mini or Claude 3 Haiku for frequent, simple tasks
       - **Quality**: Use Claude 3.5 Sonnet or GPT-4o for complex reasoning
       - **Speed**: Use smaller models or Llama 3 for latency-critical apps
       - **Context**: Use Gemini 1.5 for very long documents
    
   2. **Configure Parameters**: Adjust temperature, max_tokens based on your use case
    
    3. **Monitor Costs**: Check the Cost Tracking page to see actual costs
    
    See the [ADD_USECASE_GUIDE](./docs/ADD_USECASE_GUIDE.md) for more details.
    """)
