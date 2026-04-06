# AI Platform Hub - Project Structure Overview

## Directory Structure

```
oesl_ai_ui/
│
├── app.py                           # Main application entry point
│                                    # Routes to pages, handles navigation
│
├── config/                          # Configuration and settings
│   ├── __init__.py
│   └── settings.py                  # API keys, business units, feature flags
│
├── auth/                            # Authentication module
│   ├── __init__.py
│   └── azure_sso.py                 # Azure AD SSO implementation
│
├── pages/                           # All page components
│   ├── __init__.py
│   ├── login.py                     # Azure SSO login interface
│   ├── dashboard.py                 # Overview with key KPIs
│   ├── use_cases.py                 # Manage AI use cases
│   ├── models.py                    # Display available LLM models
│   ├── analytics.py                 # Detailed analytics (AI Team only)
│   ├── cost_tracking.py             # Cost monitoring and analysis
│   ├── performance.py               # Response times and success rates
│   ├── notifications.py             # System alerts
│   ├── activity_log.py              # Audit trail (AI Team only)
│   ├── user_feedback.py             # User ratings and comments
│   ├── settings.py                  # User preferences
│   └── admin.py                     # Admin configuration panel
│
├── components/                      # Reusable UI components
│   ├── __init__.py
│   ├── styles.py                    # CSS theming and styling
│   ├── sidebar.py                   # Navigation sidebar
│   └── logo.py                      # Logos and icons SVG
│
├── utils/                           # Utility functions
│   ├── __init__.py
│   ├── helpers.py                   # Common helper functions
│   └── charts.py                    # Chart styling and utilities
│
├── data/                            # Data models and generation
│   ├── __init__.py
│   ├── models.py                    # LLM model definitions
│   └── mock_data.py                 # Test data generation
│
├── docs/                            # Documentation
│   ├── README.md                    # Main documentation (START HERE)
│   ├── ADD_USECASE_GUIDE.md         # How to add new use cases
│   ├── API_KEYS_GUIDE.md            # API key setup instructions
│   └── DEPLOYMENT_GUIDE.md          # Production deployment
│
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
├── .streamlit/                      # Streamlit config (auto-generated)
└── README.md                        # This file
```

## Component Documentation

### Core Modules

#### `config/settings.py`
- **Purpose**: Centralized configuration management
- **Key Classes**:
  - `AzureSSO`: Azure AD configuration
  - `APIKeys`: LLM provider credentials  
  - `AppConfig`: Application settings
  - `COLOR_SCHEME`: Dark/light theme colors
- **When to Edit**: Adding new business units, API providers, or settings

#### `auth/azure_sso.py`
- **Purpose**: Azure Active Directory authentication
- **Key Classes**:
  - `AzureSSOManager`: Handles login flow and user info
- **Methods**:
  - `init_session()`: Initialize auth session state
  - `get_auth_url()`: Generate login URL
  - `get_token(auth_code)`: Exchange code for token
  - `get_user_info(token)`: Get user details from Azure AD
  - `get_user_roles(email)`: Determine user permissions

#### `data/models.py`
- **Purpose**: Define available LLM models
- **Key Classes**:
  - `LLMModel`: Represents a single model with costs/capabilities
- **When to Add**: New GPT, Claude, Gemini versions

#### `data/mock_data.py`
- **Purpose**: Generate realistic test data
- **Functions**:
  - `generate_mock_use_cases()`: Create sample use cases
  - `generate_mock_time_series()`: Generate usage data
  - `generate_all_mock_data()`: Complete dataset

### Page Components

Each page in `pages/` follows a consistent pattern:

```python
def render_[page_name]():
    """Render the [page name] page"""
    
    # 1. Header with title and description
    st.markdown('<div class="section-header">📊 Page Title</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Page description</div>', unsafe_allow_html=True)
    
    # 2. Get session data
    data = st.session_state.get("mock_data", {})
    
    # 3. Render UI components
    # Use st.columns, st.tabs for layout
    # Use st.dataframe, st.plotly_chart for displays
    
    # 4. Handle interactions
    # if st.button():...
```

### Styling System

All styles are defined in `components/styles.py`:

1. **CSS Variables** (in `<style>` tag):
   - `--bg`: Background color
   - `--surface`: Card backgrounds
   - `--accent`: Primary brand color
   - `--text`: Text color
   
2. **Themes**:
   - Dark: `#070C0A` background, `#00D98A` accent
   - Light: `#F0FAF4` background, `#00A86B` accent

3. **Custom Classes**:
   - `.metric-card`: KPI cards
   - `.uc-card`: Use case cards
   - `.badge`: Status badges
   - `.nav-item`: Sidebar items

## Data Flow

### Authentication Flow
```
User → Login Page → Azure AD → Callback → Session Set → Dashboard
```

### Page Rendering
```
app.py → Check Auth → render_sidebar() → render_[page]() → Display
```

### Data Access
```
Page → session_state["mock_data"] → Or query DB if configured
```

## Adding New Features

### Add a New Page

1. Create `pages/my_page.py`:
```python
def render_my_page():
    st.markdown('<div class="section-header">Title</div>', unsafe_allow_html=True)
    # Your content
```

2. Add to navigation in `components/sidebar.py`:
```python
nav_btn("📊", "My Page", "My Page")
```

3. Add routing in `app.py`:
```python
elif page == "My Page":
    my_page.render_my_page()
```

### Add a New Business Unit

Edit `config/settings.py`:
```python
BUSINESS_UNITS: List[str] = [
    "Marketing",
    "Operations",
    "Finance",
    "Sales",          # NEW
    "Engineering",    # NEW
]
```

### Add a New LLM Model

Edit `data/models.py`:
```python
AVAILABLE_MODELS = [
    # ... existing ...
    LLMModel(
        id="llama-3-405b",
        name="Llama 3 405B",
        provider="Meta",
        context_window="128K",
        cost_per_1k_input=0.003,
        cost_per_1k_output=0.006,
        capabilities=["Reasoning", "Code", "Analysis"]
    ),
]
```

## Testing

### Test Locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

### Add Test Use Case
Edit `data/mock_data.py`, add entry to `generate_mock_use_cases()`

### Test Authentication
Set dummy values in `.env`:
```
AZURE_CLIENT_ID=test-id
AZURE_TENANT_ID=test-tenant-id  
```

App will fall back to demo login.

## Production Readiness

- [ ] Environment variables configured
- [ ] Database connected and migrated
- [ ] Azure AD configured with correct redirect URI
- [ ] All API keys validated
- [ ] HTTPS/SSL enabled
- [ ] Rate limiting configured
- [ ] Monitoring set up
- [ ] Backups automated
- [ ] Documentation reviewed

## Key Files for Each Role

**For Business Users**:
- [README.md](docs/README.md) - Overview
- [ADD_USECASE_GUIDE.md](docs/ADD_USECASE_GUIDE.md) - Create use cases

**For Developers**:
- This file - Architecture
- `config/settings.py` - Configuration
- `pages/*.py` - Page implementations
- `components/*.py` - Reusable components

**For DevOps/Admins**:
- [DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) - Prod setup
- [API_KEYS_GUIDE.md](docs/API_KEYS_GUIDE.md) - Credentials
- `requirements.txt` - Dependencies

## Performance Tips

1. Use `@st.cache_data` for expensive operations
2. Add database indexes on common filters
3. Limit chart data points (MAX_CHART_POINTS = 100)
4. Defer loading non-critical sections
5. Monitor database query performance

## Troubleshooting

**App won't start**:
- Check `requirements.txt` installed: `pip list`
- Check `.env` exists and is valid
- Run with `--logger.level=debug`

**No mock data**:
- Check `ENABLE_MOCK_DATA=true` in `.env`
- Restart Streamlit

**Azure login loop**:
- Verify CLIENT_ID, TENANT_ID, SECRET in `.env`
- Check redirect URI matches Azure app registration
- Must use HTTPS for production redirect URIs

See [DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) for production issues.

---

**Version**: 2.0.0 | **Last Updated**: April 6, 2026
