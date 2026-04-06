"""
Configuration and Settings
Handles all environment variables, API keys, and application settings.
Production-ready configuration with secure defaults.
"""

import os
from typing import Dict, List
from dataclasses import dataclass, field


@dataclass
class AzureSSO:
    """Azure Active Directory SSO Configuration"""
    # Azure AD Application (client) ID
    CLIENT_ID: str = os.getenv("AZURE_CLIENT_ID", "your-client-id-here")
    
    # Azure AD tenant ID
    TENANT_ID: str = os.getenv("AZURE_TENANT_ID", "your-tenant-id-here")
    
    # Azure AD Application secret
    CLIENT_SECRET: str = os.getenv("AZURE_CLIENT_SECRET", "your-client-secret-here")
    
    # OAuth2 scopes for AD
    SCOPES: List[str] = ["https://graph.microsoft.com/.default"]
    
    # Redirect URI (must match Azure app registration)
    REDIRECT_URI: str = os.getenv("AZURE_REDIRECT_URI", "http://localhost:8501/auth/callback")
    
    # Azure authorization endpoint
    AUTHORITY_URL: str = f"https://login.microsoftonline.com/{TENANT_ID}"
    
    # Token endpoint
    TOKEN_URL: str = f"{AUTHORITY_URL}/oauth2/v2.0/token"
    
    # Authorization endpoint
    AUTH_URL: str = f"{AUTHORITY_URL}/oauth2/v2.0/authorize"


@dataclass
class APIKeys:
    """API Keys Configuration for LLM Providers
    
    These should be stored in environment variables for security:
    - OPENAI_API_KEY: For GPT-4, GPT-4o, GPT-3.5-turbo
    - ANTHROPIC_API_KEY: For Claude models
    - GOOGLE_API_KEY: For Gemini models
    - MISTRAL_API_KEY: For Mistral models
    """
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY", "")
    AZURE_OPENAI_KEY: str = os.getenv("AZURE_OPENAI_KEY", "")
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")


@dataclass
class AppConfig:
    """Main Application Configuration"""
    
    # App metadata
    APP_TITLE: str = "AI Platform Hub"
    APP_ICON: str = "⬡"
    APP_DESCRIPTION: str = "Enterprise Use Case Management Platform"
    APP_VERSION: str = "2.0.0"
    
    # Layout
    LAYOUT: str = "wide"
    SIDEBAR_STATE: str = "expanded"
    
    # Theme defaults
    DARK_MODE_DEFAULT: bool = True
    
    # Pagination and limits
    ITEMS_PER_PAGE: int = 20
    MAX_CHART_POINTS: int = 100
    CACHE_TIMEOUT_SECONDS: int = 3600
    
    # Feature flags
    ENABLE_MOCK_DATA: bool = True  # Use mock data if True, connect to real DB if False
    ENABLE_ANALYTICS: bool = True
    ENABLE_COST_TRACKING: bool = True
    ENABLE_PERFORMANCE_MONITORING: bool = True
    
    # Chart settings
    CHART_HEIGHT_DEFAULT: int = 300
    CHART_THEME: Dict = None  # Set in app initialization based on dark mode
    
    # Business Units (Departments) - Add new departments here
    BUSINESS_UNITS: List[str] = field(default_factory=lambda: [
        "Marketing",
        "Operations", 
        "Finance",
        "Sales",
        "HR",
        "Product",
        "Engineering",
        # Add new departments here
    ])


# Initialize global config
azure_sso = AzureSSO()
api_keys = APIKeys()
config = AppConfig()


def get_config() -> AppConfig:
    """Get global configuration object"""
    return config


def get_azure_sso() -> AzureSSO:
    """Get Azure SSO configuration"""
    return azure_sso


def get_api_keys() -> APIKeys:
    """Get API keys configuration"""
    return api_keys


def validate_azure_sso() -> bool:
    """Validate that Azure SSO is properly configured"""
    required_vars = [
        azure_sso.CLIENT_ID,
        azure_sso.TENANT_ID,
        azure_sso.CLIENT_SECRET,
    ]
    return all(var and var != "your-" + var.split("-")[0] + "-id-here" 
               for var in required_vars)


def validate_api_keys(provider: str) -> bool:
    """Validate API key for a specific provider"""
    provider_map = {
        "openai": api_keys.OPENAI_API_KEY,
        "anthropic": api_keys.ANTHROPIC_API_KEY,
        "google": api_keys.GOOGLE_API_KEY,
        "mistral": api_keys.MISTRAL_API_KEY,
        "azure": api_keys.AZURE_OPENAI_KEY,
    }
    key = provider_map.get(provider.lower(), "")
    return bool(key and key.strip())


# Color scheme (can be extended)
COLOR_SCHEME = {
    "dark": {
        "bg": "#070C0A",
        "surface": "#0C1410",
        "surface2": "#111C16",
        "border": "#1A2E22",
        "text": "#DFF0E6",
        "text2": "#6B9478",
        "accent": "#00D98A",
        "accent2": "#FFB020",
        "green": "#00D98A",
        "red": "#FF4D6A",
        "orange": "#FFB020",
        "card_bg": "#0C1410",
    },
    "light": {
        "bg": "#F0FAF4",
        "surface": "#FFFFFF",
        "surface2": "#E4F5EC",
        "border": "#B8DCCA",
        "text": "#091912",
        "text2": "#3D6E54",
        "accent": "#00A86B",
        "accent2": "#D4890A",
        "green": "#00A86B",
        "red": "#D93B55",
        "orange": "#D4890A",
        "card_bg": "#FFFFFF",
    }
}
