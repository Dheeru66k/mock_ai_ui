# API Keys Setup Guide

This guide explains how to configure API keys for different LLM providers in production.

## 🔐 Security Best Practices

### Rule 1: Never Commit API Keys
Always use environment variables. **NEVER** hardcode keys in files.

```python
# ❌ BAD - Never do this
API_KEY = "sk-proj-abc123xyz"

# ✅ GOOD - Use environment variables
API_KEY = os.getenv("OPENAI_API_KEY", "")
```

### Rule 2: Use Secrets Management
For production, use:
- **Azure Key Vault** (if using Azure)
- **AWS Secrets Manager** (if using AWS)
- **HashiCorp Vault** (on-premise)
- **Kubernetes Secrets** (if K8s)

### Rule 3: Rotate Keys Regularly
- Rotate keys every 90 days
- Use versioning for seamless rotation
- Never remove old key immediately

## Environment Variables

Create a `.env` file in the project root (never commit this):

```bash
# .env (DO NOT COMMIT TO GIT)

#  OpenAI API Keys
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
OPENAI_ORG_ID=org-xxxxxxxxxx  # Optional, for org-level access

# Anthropic (Claude)
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxx

# Google Gemini
GOOGLE_API_KEY=XXXXXXXXXXXXXXXXXXXXXXXX

# Mistral AI
MISTRAL_API_KEY=XXXXXXXXXXXXXXXXXXXXXXXX

# Azure OpenAI
AZURE_OPENAI_KEY=XXXXXXXXXXXXXXXX
AZURE_OPENAI_ENDPOINT=https://xxxx.openai.azure.com/
AZURE_OPENAI_VERSION=2024-02-15-preview

# Azure Active Directory (for SSO)
AZURE_CLIENT_ID=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
AZURE_TENANT_ID=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
AZURE_CLIENT_SECRET=XXXXXXXXXXXXXXXXXXXXXXXX
AZURE_REDIRECT_URI=https://yourdomain.com/auth/callback

# Database (if using real DB)
DATABASE_URL=postgresql://user:password@localhost/oesl_ai_ui
```

### Loading Environment Variables

```python
# Python automatically loads from .env
import os
from config.settings import api_keys

# Access keys
openai_key = api_keys.OPENAI_API_KEY
```

Or manually with python-dotenv:

```python
from dotenv import load_dotenv
import os

load_dotenv()  # Load from .env file
openai_key = os.getenv("OPENAI_API_KEY")
```

## Provider Setup

### 1. OpenAI (GPT-4, GPT-4o, GPT-3.5-turbo)

**Cost**: Pay-per-use (reasonable for most uses)

**Setup Steps**:

1. Go to https://platform.openai.com/account/api-keys
2. Click "Create new secret key"
3. Copy the key: `sk-proj-...`
4. Add to `.env`:
   ```bash
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
   ```
5. Test:
   ```python
   import openai
   from config.settings import api_keys
   
   client = openai.Client(api_key=api_keys.OPENAI_API_KEY)
   response = client.chat.completions.create(
       model="gpt-4o",
       messages=[{"role": "user", "content": "Hello"}]
   )
   print(response.choices[0].message.content)
   ```

**Pricing**:
- GPT-4o: $5/$15 per 1M tokens (input/output)
- GPT-4o Mini: $0.15/$0.60 per 1M tokens
- GPT-3.5-turbo: $0.50/$1.50 per 1M tokens

**Setup Cost Controls**:

```python
# pages/settings.py - Add cost limit reminder
st.warning("Budget: $100/month")

# Query API for usage
client = openai.Client(api_key=api_keys.OPENAI_API_KEY)
usage = client.usage.list()  # Not all models support this
print(f"Used: ${usage.total_usage}")
```

### 2. Anthropic (Claude)

**Cost**: Similar to OpenAI

**Setup Steps**:

1. Go to https://console.anthropic.com/
2. Click "Create key" in API keys section
3. Copy the key: `sk-ant-...`
4. Add to `.env`:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxx
   ```
5. Test:
   ```python
   import anthropic
   from config.settings import api_keys
   
   client = anthropic.Anthropic(api_key=api_keys.ANTHROPIC_API_KEY)
   response = client.messages.create(
       model="claude-3-5-sonnet-20241022",
       max_tokens=1024,
       messages=[{"role": "user", "content": "Hello"}]
   )
   print(response.content[0].text)
   ```

**Pricing**:
- Claude 3.5 Sonnet: $3/$15 per 1M tokens
- Claude 3 Opus: $15/$75 per 1M tokens
- Claude 3 Haiku: $0.25/$1.25 per 1M tokens

### 3. Google Gemini

**Cost**: Free tier available, paid plans start $10/month

**Setup Steps**:

1. Go to https://ai.google.dev/pricing
2. Click "Create API Key" (free tier)
3. Copy the key
4. Add to `.env`:
   ```bash
   GOOGLE_API_KEY=XXXXXXXXXXXXXXXXXXXXXXXX
   ```
5. Test:
   ```python
   import google.generativeai as genai
   from config.settings import api_keys
   
   genai.configure(api_key=api_keys.GOOGLE_API_KEY)
   model = genai.GenerativeModel('gemini-pro')
   response = model.generate_content("Hello")
   print(response.text)
   ```

**Pricing**:
- Gemini 1.5 Pro: Free tier (60 calls/min), then $10/1M input tokens

### 4. Azure OpenAI

**Cost**: Fixed pricing, good for enterprise

**Setup Steps**:

1. Go to Azure Portal → Create resource → "Azure OpenAI"
2. Create deployment with:
   - Model: `gpt-4o` or `gpt-4-turbo`
   - Version: Latest
3. Go to Keys and Endpoint
4. Add to `.env`:
   ```bash
   AZURE_OPENAI_KEY=XXXXXXXXXXXXXXXX
   AZURE_OPENAI_ENDPOINT=https://xxxx.openai.azure.com/
   AZURE_OPENAI_VERSION=2024-02-15-preview
   ```
5. Test:
   ```python
   from openai import AzureOpenAI
   from config.settings import api_keys
   
   client = AzureOpenAI(
       api_key=api_keys.AZURE_OPENAI_KEY,
       api_version=api_keys.AZURE_OPENAI_VERSION,
       azure_endpoint=api_keys.AZURE_OPENAI_ENDPOINT
   )
   # Use like normal OpenAI client
   ```

### 5. Mistral AI

**Cost**: Competitive pricing

**Setup Steps**:

1. Go to https://console.mistral.ai/
2. Create API key
3. Add to `.env`:
   ```bash
   MISTRAL_API_KEY=XXXXXXXXXXXXXXXXXXXXXXXX
   ```
4. Test:
   ```python
   from mistralai.client import MistralClient
   from config.settings import api_keys
   
   client = MistralClient(api_key=api_keys.MISTRAL_API_KEY)
   response = client.chat(
       model="mistral-medium",
       messages=[{"role": "user", "content": "Hello"}]
   )
   ```

## Cost Monitoring

### Track API Costs

Create `utils/cost_tracker.py`:

```python
import os
from datetime import datetime
from typing import Dict
import json

class CostTracker:
    """Track costs for different models"""
    
    COSTS_PER_1M_TOKENS = {
        "gpt-4o": {"input": 5, "output": 15},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "claude-3-5-sonnet": {"input": 3, "output": 15},
        "claude-3-haiku": {"input": 0.25, "output": 1.25},
        "gemini-1-5-pro": {"input": 1.75, "output": 3.50},
    }
    
    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for a single API call"""
        if model not in self.COSTS_PER_1M_TOKENS:
            return 0.0
        
        costs = self.COSTS_PER_1M_TOKENS[model]
        input_cost = (input_tokens / 1_000_000) * costs["input"]
        output_cost = (output_tokens / 1_000_000) * costs["output"]
        return input_cost + output_cost
    
    def log_usage(self, use_case_id: str, model: str, tokens: int, cost: float):
        """Log usage to a file or database"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "use_case_id": use_case_id,
            "model": model,
            "tokens": tokens,
            "cost": cost,
        }
        
        # Save to file (in production, use database)
        with open("usage_log.jsonl", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
```

### Cost Alerts

In `pages/settings.py`, add cost warnings:

```python
import streamlit as st
from config.settings import config

def render_settings():
    st.markdown("## Cost Alerts")
    
    budget = st.number_input("Monthly Budget ($)", value=1000, step=100)
    
    # Check current spending
    current_spend = sum(uc["monthly_cost"] for uc in use_cases)
    
    if current_spend > budget * 0.8:
        st.warning(f"⚠️ Spending at {(current_spend/budget)*100:.0f}% of budget!")
    
    if current_spend > budget:
        st.error("🚨 Budget exceeded!")
```

## Production Deployment

### Using Azure Key Vault

```python
# config/settings.py
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def get_api_key(key_name: str) -> str:
    """Get API key from Azure Key Vault"""
    
    vault_url = "https://yourvault.vault.azure.net/"
    
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    
    secret = client.get_secret(key_name)
    return secret.value

# Usage
api_keys.OPENAI_API_KEY = get_api_key("openai-api-key")
```

### Using GitHub Secrets (for CI/CD)

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          AZURE_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
        run: |
          pip install -r requirements.txt
          streamlit run app.py
```

## Troubleshooting

### "API key error" or "401 Unauthorized"

1. Check key is correct (copy-paste carefully)
2. Verify key has right permissions
3. Check key hasn't been revoked
4. Ensure OPENAI_API_KEY is being read:
   ```python
   import os
   print(os.getenv("OPENAI_API_KEY"))  # Should show key
   ```

### Rate Limit Errors

Implement retry logic:

```python
import time
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
def call_api_with_retry(client, **kwargs):
    return client.chat.completions.create(**kwargs)
```

### High Unexpected Costs

1. Check for runaway production deployments
2. Review active use cases (cost_tracking page)
3. Lower `max_tokens` parameter if possible
4. Switch to cheaper models (GPT-4o Mini vs GPT-4o)
5. Set hard spending limits at provider level

## Next Steps

1. Generate your API keys from each provider
2. Add them to `.env`
3. Test connectivity in `pages/settings.py`
4. Start using AI in your use cases
5. Monitor costs weekly

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for production setup.
