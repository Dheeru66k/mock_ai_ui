"""
LLM Model Definitions and Configurations
Defines all available AI models with their capabilities and costs.
"""

from typing import List, Dict


class LLMModel:
    """Represents an LLM model with its configuration"""
    
    def __init__(
        self,
        id: str,
        name: str,
        provider: str,
        context_window: str,
        cost_per_1k_input: float,
        cost_per_1k_output: float,
        status: str = "active",
        capabilities: List[str] = None
    ):
        self.id = id
        self.name = name
        self.provider = provider
        self.context_window = context_window
        self.cost_per_1k_input = cost_per_1k_input
        self.cost_per_1k_output = cost_per_1k_output
        self.status = status
        self.capabilities = capabilities or []
    
    def to_dict(self) -> Dict:
        """Convert to dictionary representation"""
        return {
            "id": self.id,
            "name": self.name,
            "provider": self.provider,
            "context": self.context_window,
            "cost_input": self.cost_per_1k_input,
            "cost_output": self.cost_per_1k_output,
            "status": self.status,
            "strengths": self.capabilities,
        }


# Define all available models
AVAILABLE_MODELS = [
    LLMModel(
        id="gpt-4o",
        name="GPT-4o",
        provider="OpenAI",
        context_window="128K",
        cost_per_1k_input=0.005,
        cost_per_1k_output=0.015,
        capabilities=["Reasoning", "Vision", "Code", "Complex Analysis"]
    ),
    LLMModel(
        id="gpt-4o-mini",
        name="GPT-4o Mini",
        provider="OpenAI",
        context_window="128K",
        cost_per_1k_input=0.00015,
        cost_per_1k_output=0.0006,
        capabilities=["Speed", "Cost Efficiency", "General Purpose"]
    ),
    LLMModel(
        id="claude-3-5-sonnet",
        name="Claude 3.5 Sonnet",
        provider="Anthropic",
        context_window="200K",
        cost_per_1k_input=0.003,
        cost_per_1k_output=0.015,
        capabilities=["Writing", "Analysis", "Safety","Long Context"]
    ),
    LLMModel(
        id="claude-3-haiku",
        name="Claude 3 Haiku",
        provider="Anthropic",
        context_window="200K",
        cost_per_1k_input=0.00025,
        cost_per_1k_output=0.00125,
        capabilities=["Speed", "Cost Efficiency", "Summarization"]
    ),
    LLMModel(
        id="gemini-1-5-pro",
        name="Gemini 1.5 Pro",
        provider="Google",
        context_window="1M",
        cost_per_1k_input=0.00175,
        cost_per_1k_output=0.0035,
        capabilities=["Long Context", "Multimodal", "Code Analysis"]
    ),
    LLMModel(
        id="llama-3-70b",
        name="Llama 3 70B",
        provider="Meta/Self-Hosted",
        context_window="8K",
        cost_per_1k_input=0.0005,
        cost_per_1k_output=0.0015,
        capabilities=["Open Source", "Privacy", "Self-Hosted"]
    ),
    LLMModel(
        id="mistral-large",
        name="Mistral Large",
        provider="Mistral AI",
        context_window="32K",
        cost_per_1k_input=0.002,
        cost_per_1k_output=0.006,
        capabilities=["European Compliance", "Reasoning", "Code"]
    ),
]


def get_all_models() -> List[Dict]:
    """Get all available models as dictionaries"""
    return [model.to_dict() for model in AVAILABLE_MODELS]


def get_model_by_id(model_id: str) -> LLMModel:
    """Get a model by its ID"""
    for model in AVAILABLE_MODELS:
        if model.id == model_id:
            return model
    raise ValueError(f"Model not found: {model_id}")


def get_models_by_provider(provider: str) -> List[LLMModel]:
    """Get all models from a specific provider"""
    return [m for m in AVAILABLE_MODELS if m.provider == provider.lower()]


def get_active_models() -> List[LLMModel]:
    """Get only active (non-deprecated) models"""
    return [m for m in AVAILABLE_MODELS if m.status == "active"]
