# How to Add New Use Cases

This guide explains how to add new AI use cases to the AI Platform Hub.

## Overview

A **use case** represents a specific AI task your organization uses. Examples:
- "Campaign Copy Generator" (Marketing)
- "Expense Anomaly Detector" (Finance)
- "Incident Report Summarizer" (Operations)

## Quick Start: 3 Steps

### Step 1: Add Use Case to Mock Data

Edit `data/mock_data.py`:

```python
def generate_mock_use_cases() -> List[Dict]:
    """Generate mock use case data"""
    use_cases = [
        # ... existing use cases ...
        
        # YOUR NEW USE CASE
        {
            "id": "uc-099",  # Unique ID
            "name": "My Awesome Use Case",
            "description": "What this use case does in detail.",
            "owner": "owner@company.com",
            "owner_name": "Owner Name",
            "business_unit": "Marketing",  # Must be in BUSINESS_UNITS
            "type": "Content Generation",  # See available types below
            "status": "active",  # active, draft, inactive
            "model": "gpt-4o-mini",  # See data/models.py for available
            "created": now - timedelta(days=45),
            "last_accessed": now - timedelta(hours=2),
            "usage_count": 1500,  # Monthly API calls
            "monthly_cost": 45.30,  # Monthly cost
            "avg_response_ms": 800,  # Average response time
            "success_rate": 98.5,  # Success rate percentage
            "users": ["user-group-1", "user-group-2"],
            "tags": ["tag1", "tag2"],
            "params": {
                "temperature": 0.7,  # Model creativity (0-1)
                "max_tokens": 1024,  # Max output length
                "top_p": 0.95,  # Nucleus sampling
                "frequency_penalty": 0.1,
                "presence_penalty": 0.1,
            },
        },
    ]
    return use_cases
```

### Step 2: Available Use Case Types

```
- Content Generation
- Text Analysis
- Summarization
- Document Review
- Data Analysis
- Report Generation
- Anomaly Detection
- Code Generation
- Chat/Conversation
- Other
```

Add icon for your type in `components/logo.py`, `get_usecase_icon_svg()` if needed.

### Step 3: Verify in Dashboard

1. Run: `streamlit run app.py`
2. Navigate to "Use Cases" page
3. Your new use case should appear in the list

## Production Setup: Real Database

For production, instead of mock data, integrate with a real database:

### Option A: PostgreSQL (Recommended)

```python
# data/database.py (NEW FILE)
import psycopg2
from typing import List, Dict

class UseCaseDB:
    def __init__(self, connection_string):
        self.conn = psycopg2.connect(connection_string)
    
    def create_use_case(self, data: Dict) -> str:
        """Create a new use case"""
        cur = self.conn.cursor()
        sql = """
            INSERT INTO use_cases 
            (id, name, description, owner, business_unit, model, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        cur.execute(sql, (
            data["id"],
            data["name"],
            data["description"],
            data["owner"],
            data["business_unit"],
            data["model"],
            data["status"]
        ))
        self.conn.commit()
        return cur.fetchone()[0]
    
    def get_all_use_cases(self) -> List[Dict]:
        """Get all use cases"""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM use_cases")
        # Convert to dict...
        return use_cases

# config/settings.py
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost/oesl_ai_ui"
)
ENABLE_MOCK_DATA = False  # Switch to False for production
```

### Schema Example

```sql
CREATE TABLE use_cases (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    owner VARCHAR(255),
    owner_name VARCHAR(255),
    business_unit VARCHAR(100),
    type VARCHAR(100),
    status VARCHAR(50),
    model VARCHAR(100),
    created_at TIMESTAMP,
    last_accessed TIMESTAMP,
    usage_count INTEGER,
    monthly_cost DECIMAL(10, 2),
    avg_response_ms INTEGER,
    success_rate DECIMAL(5, 2),
    config JSONB,  -- Store params as JSON
    created_by VARCHAR(255),
    updated_at TIMESTAMP
);

CREATE INDEX idx_business_unit ON use_cases(business_unit);
CREATE INDEX idx_status ON use_cases(status);
CREATE INDEX idx_owner ON use_cases(owner);
```

## API Integration

To actually call the AI models:

```python
# utils/llm_client.py (NEW FILE)
from config.settings import api_keys
import openai
import anthropic

class LLMClient:
    """Unified interface for different LLM providers"""
    
    def __init__(self):
        self.openai_client = openai.Client(api_key=api_keys.OPENAI_API_KEY)
        self.anthropic_client = anthropic.Anthropic(api_key=api_keys.ANTHROPIC_API_KEY)
    
    def call_model(self, model_id: str, prompt: str, params: Dict) -> str:
        """Call an LLM model"""
        
        if model_id.startswith("gpt"):
            return self._call_openai(model_id, prompt, params)
        elif model_id.startswith("claude"):
            return self._call_anthropic(model_id, prompt, params)
        else:
            raise ValueError(f"Unknown model: {model_id}")
    
    def _call_openai(self, model: str, prompt: str, params: Dict) -> str:
        response = self.openai_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=params.get("temperature", 0.7),
            max_tokens=params.get("max_tokens", 1024),
            top_p=params.get("top_p", 0.95),
        )
        return response.choices[0].message.content
    
    def _call_anthropic(self, model: str, prompt: str, params: Dict) -> str:
        response = self.anthropic_client.messages.create(
            model=model,
            max_tokens=params.get("max_tokens", 1024),
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

# In pages/use_cases.py
from utils.llm_client import LLMClient

llm = LLMClient()

if st.button("Test Use Case"):
    result = llm.call_model(
        uc["model"],
        "Your test prompt",
        uc["params"]
    )
    st.write(result)
```

## Add New Department/Business Unit

Edit `config/settings.py`:

```python
BUSINESS_UNITS: List[str] = [
    "Marketing",
    "Operations",
    "Finance",
    "Sales",           # Add here
    "Engineering",     # Add here
    "Your Department", # Add here
]
```

These values will:
- Appear in department filters
- Show in sidebar navigation
- Be trackable for cost allocation
- Determine role-based access

## Complete Example: Adding "Sales Pitch Generator"

### 1. Add to mock_data.py:

```python
{
    "id": "uc-010",
    "name": "Sales Pitch Generator",
    "description": "Generates personalized sales pitches based on customer profile.",
    "owner": "john.sales@company.com",
    "owner_name": "John Sales",
    "business_unit": "Sales",
    "type": "Content Generation",
    "status": "active",
    "model": "claude-3-5-sonnet",
    "created": now - timedelta(days=30),
    "last_accessed": now - timedelta(hours=1),
    "usage_count": 2100,
    "monthly_cost": 156.80,
    "avg_response_ms": 1450,
    "success_rate": 97.6,
    "users": ["sales-team", "account-managers"],
    "tags": ["sales", "personalization"],
    "params": {
        "temperature": 0.8,
        "max_tokens": 1500,
        "top_p": 0.95,
        "frequency_penalty": 0.2,
        "presence_penalty": 0.2,
    },
}
```

### 2. Ensure "Sales" is in BUSINESS_UNITS (config/settings.py)

### 3. Run app and check Use Cases page

```bash
streamlit run app.py
```

## Monitoring Your Use Case

Once created, monitor it via:

1. **Dashboard**: KPI cards show usage and cost
2. **Cost Tracking**: See monthly expenses
3. **Analytics**: Track usage trends
4. **Performance**: Monitor response times
5. **User Feedback**: Gather user ratings

## Best Practices

✅ **Do:**
- Use descriptive names and descriptions
- Set realistic usage estimates for cost tracking
- Document the model choice reasoning
- Monitor feedback and adjust parameters
- Start as "draft", move to "active" after testing

❌ **Don't:**
- Use test IDs in production (use uc-XXXX format)
- Hardcode API keys (use environment variables)
- Forget to add to correct business unit
- Leave unused use cases in "active" status
- Skip parameter tuning for your use case

## Troubleshooting

### Use case not appearing
- Check if status is "active" or desired status
- Verify business_unit is in BUSINESS_UNITS
- Restart Streamlit: `streamlit run app.py`

### Wrong cost calculation
- Check usage_count and monthly_cost match your actual usage
- Verify model's cost_per_1k token settings (data/models.py)
- Recalculate: usage_count * (monthly_cost / usage_count)

### Parameter not affecting output
- Check param names match the model's API spec
- Use Streamlit's `st.write()` to debug params
- Test via pages/models.py "Test Use Case" section

## Next Steps

1. Add more use cases in your department
2. Track performance metrics
3. Optimize parameters based on feedback
4. Scale successful use cases
5. Archive underperforming ones

See [ADD_DEPARTMENT_GUIDE.md](ADD_DEPARTMENT_GUIDE.md) for adding new departments.
