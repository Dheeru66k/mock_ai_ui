"""
Azure Active Directory SSO Authentication
Handles user authentication via Azure AD with MSAL (Microsoft Authentication Library).
"""

import streamlit as st
import json
from typing import Dict, Optional
from datetime import datetime
import requests
from config.settings import azure_sso, config


class AzureSSOManager:
    """Manages Azure AD authentication flow"""
    
    def __init__(self):
        self.azure_config = azure_sso
        self.initialized = False
    
    def init_session(self):
        """Initialize session state variables for authentication"""
        if "auth_token" not in st.session_state:
            st.session_state.auth_token = None
        if "user_info" not in st.session_state:
            st.session_state.user_info = None
        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False
        if "login_timestamp" not in st.session_state:
            st.session_state.login_timestamp = None
    
    def get_auth_url(self, state: str = "security_token") -> str:
        """Generate Azure AD login URL
        
        Args:
            state: Security state parameter for CSRF protection
            
        Returns:
            Complete Azure AD authorization URL
        """
        params = {
            "client_id": self.azure_config.CLIENT_ID,
            "response_type": "code",
            "scope": " ".join(self.azure_config.SCOPES),
            "redirect_uri": self.azure_config.REDIRECT_URI,
            "response_mode": "query",
            "state": state,
            "prompt": "select_account"
        }
        
        query_string = "&".join(
            f"{key}={value}" for key, value in params.items()
        )
        return f"{self.azure_config.AUTH_URL}/oauth2/v2.0/authorize?{query_string}"
    
    def get_token(self, auth_code: str) -> Optional[Dict]:
        """Exchange authorization code for access token
        
        Args:
            auth_code: Authorization code from Azure AD callback
            
        Returns:
            Token response dictionary or None if failed
        """
        token_data = {
            "client_id": self.azure_config.CLIENT_ID,
            "client_secret": self.azure_config.CLIENT_SECRET,
            "code": auth_code,
            "redirect_uri": self.azure_config.REDIRECT_URI,
            "grant_type": "authorization_code",
            "scope": " ".join(self.azure_config.SCOPES),
        }
        
        try:
            response = requests.post(self.azure_config.TOKEN_URL, json=token_data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            st.error(f"Token exchange failed: {str(e)}")
            return None
    
    def get_user_info(self, access_token: str) -> Optional[Dict]:
        """Fetch user information from Microsoft Graph API
        
        Args:
            access_token: Valid access token from Azure AD
            
        Returns:
            User information dictionary or None if failed
        """
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        
        try:
            response = requests.get(
                "https://graph.microsoft.com/v1.0/me",
                headers=headers
            )
            response.raise_for_status()
            user_data = response.json()
            
            # Fetch user's organizational info
            office_location = self._get_user_department(access_token)
            user_data["department"] = office_location or "General"
            
            return user_data
        except requests.RequestException as e:
            st.error(f"Failed to fetch user info: {str(e)}")
            return None
    
    def _get_user_department(self, access_token: str) -> Optional[str]:
        """Get user's department from Azure AD
        
        Args:
            access_token: Valid access token
            
        Returns:
            Department name or None
        """
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        
        try:
            response = requests.get(
                "https://graph.microsoft.com/v1.0/me?$select=department,officeLocation",
                headers=headers
            )
            response.raise_for_status()
            data = response.json()
            return data.get("department") or data.get("officeLocation")
        except:
            return None
    
    def set_logged_in(self, user_info: Dict, token: Dict):
        """Set session state to logged in
        
        Args:
            user_info: User information from Azure AD
            token: Token response
        """
        st.session_state.logged_in = True
        st.session_state.user_info = user_info
        st.session_state.auth_token = token.get("access_token")
        st.session_state.login_timestamp = datetime.now().isoformat()
        st.session_state.active_page = "dashboard"
    
    def logout(self):
        """Clear session state to log out"""
        st.session_state.logged_in = False
        st.session_state.user_info = None
        st.session_state.auth_token = None
        st.session_state.login_timestamp = None
    
    def is_authenticated(self) -> bool:
        """Check if user is currently authenticated"""
        return st.session_state.get("logged_in", False)
    
    def get_current_user(self) -> Optional[Dict]:
        """Get currently logged in user's information"""
        return st.session_state.get("user_info")
    
    def get_user_email(self) -> Optional[str]:
        """Get current user's email"""
        user = self.get_current_user()
        return user.get("mail") or user.get("userPrincipalName") if user else None
    
    def get_user_roles(self, email: str) -> list:
        """Get user roles/groups from Azure AD
        
        For production, this should query Azure AD groups.
        Default implementation returns role based on department.
        
        Args:
            email: User email
            
        Returns:
            List of role names
        """
        user = self.get_current_user()
        if not user:
            return []
        
        # Default role assignment based on department
        # In production, query Azure AD groups instead
        department = user.get("department", "").lower()
        
        roles = ["User"]  # Everyone has User role
        
        # Map departments to roles (customize as needed)
        if any(d in department for d in ["finance", "accounting"]):
            roles.append("Finance")
        if any(d in department for d in ["marketing", "communications"]):
            roles.append("Marketing")
        if any(d in department for d in ["operations", "ops"]):
            roles.append("Operations")
        if any(d in department for d in ["ai", "data", "engineering"]):
            roles.append("AI Team")
        if "admin" in department or email.endswith("@admin.local"):
            roles.append("Admin")
        
        return roles


# Global SSO manager instance
sso_manager = AzureSSOManager()


def get_sso_manager() -> AzureSSOManager:
    """Get global SSO manager instance"""
    return sso_manager


def get_demo_user() -> Dict:
    """Get a demo user for testing purposes
    
    Returns:
        Dictionary with demo user information
    """
    return {
        "id": "demo-user-123",
        "displayName": "Demo User",
        "mail": "demo@aiplatform.local",
        "userPrincipalName": "demo@aiplatform.local",
        "givenName": "Demo",
        "surname": "User",
        "department": "AI Team",
        "officeLocation": "Headquarters",
        "jobTitle": "AI Engineer",
        "mobilePhone": "+1-555-0100"
    }
