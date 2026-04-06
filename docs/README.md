# AI Platform Hub - Enterprise Use Case Management

Comprehensive, production-ready Streamlit application for managing AI use cases across your enterprise.

## 🎯 Key Features

- **Azure AD SSO Integration**: Enterprise authentication via Microsoft Azure AD
- **Use Case Management**: Create, monitor, and optimize AI use cases
- **Cost Tracking**: Monitor spending across models and departments
- **Performance Monitoring**: Track response times and success rates
- **Multi-Department Support**: Tailored views for different business units
- **Modular Architecture**: Clean separation of concerns for easy maintenance
- **Production Ready**: Comprehensive error handling and security practices

## 📁 Project Structure

```
oesl_ai_ui/
├── app.py                      # Main application entry point
├── config/
│   └── settings.py             # Configuration, API keys, environment variables
├── auth/
│   └── azure_sso.py            # Azure AD authentication manager
├── pages/                       # All page components
│   ├── login.py                # Login page with Azure SSO
│   ├── dashboard.py            # Main dashboard
│   ├── use_cases.py            # Use case management
│   ├── models.py               # Available LLM models
│   ├── analytics.py            # Detailed analytics
│   ├── cost_tracking.py        # Cost monitoring and analysis
│   ├── performance.py          # Performance metrics
│   ├── notifications.py        # System notifications
│   ├── settings.py             # User and app settings
│   ├── activity_log.py         # Audit trail
│   ├── user_feedback.py        # User feedback and ratings
│   └── admin.py                # Admin panel
├── components/                  # Reusable components
│   ├── styles.py               # CSS styling and theme
│   ├── sidebar.py              # Navigation sidebar
│   └── logo.py                 # Logo and icons
├── utils/                       # Utility functions
│   ├── helpers.py              # Common helper functions
│   └── charts.py               # Chart styling and creation
├── data/                        # Data models and generation
│   ├── models.py               # LLM model definitions
│   └── mock_data.py            # Mock data generation
├── docs/                        # Documentation
│   ├── README.md               # This file
│   ├── ADD_USECASE_GUIDE.md    # How to add new use cases
│   ├── API_KEYS_GUIDE.md       # API keys setup
│   └── DEPLOYMENT_GUIDE.md     # Production deployment
├── requirements.txt            # Python dependencies
└── .env.example                # Environment variables template
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
cd /home/dheerus/Desktop/oesl_ai_ui
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the template and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add:
- `OPENAI_API_KEY`: Your OpenAI API key
- `ANTHROPIC_API_KEY`: Your Anthropic/Claude API key
- `GOOGLE_API_KEY`: Your Google Gemini API key
- Azure AD credentials (for SSO)

### 3. Run the Application

```bash
streamlit run app.py
```

Visit `http://localhost:8501` in your browser.

## 🔐 Azure AD Configuration

### For Production (Real SSO)

1. Register an app in Azure AD:
   - Go to Azure Portal → App registrations
   - Create new registration
   - Set redirect URI: `https://yourdomain.com/auth/callback`
   - Create a client secret

2. Set environment variables:
   ```bash
   AZURE_CLIENT_ID=your_client_id
   AZURE_TENANT_ID=your_tenant_id
   AZURE_CLIENT_SECRET=your_client_secret
   AZURE_REDIRECT_URI=https://yourdomain.com/auth/callback
   ```

3. Update auth_sso.py if needed for group-based role assignment

### For Development (Demo Mode)

The app includes a demo fallback when Azure AD isn't configured. Just run it and sign in with the demo email.

## 📖 Key Documentation

### [Add New Use Case](docs/ADD_USECASE_GUIDE.md)
Learn how to add new AI use cases to the platform.

### [API Keys Setup](docs/API_KEYS_GUIDE.md)
Complete guide to configuring API keys for different LLM providers.

### [Production Deployment](docs/DEPLOYMENT_GUIDE.md)
Deploy the application to production with proper configurations.

## 🎨 Customization

### Add New Department/Business Unit

1. Edit `config/settings.py`:

```python
BUSINESS_UNITS: List[str] = [
    "Marketing",
    "Operations",
    "Finance",
    "Sales",        # Add here
    "Your Department",
]
```

### Add New LLM Model

1. Edit `data/models.py`:

```python
AVAILABLE_MODELS = [
    # ... existing models ...
    LLMModel(
        id="your-model-id",
        name="Your Model Name",
        provider="Your Provider",
        context_window="128K",
        cost_per_1k_input=0.001,
        cost_per_1k_output=0.002,
        capabilities=["Feature1", "Feature2"],
    ),
]
```

### Add New Report/Analytics

1. Create a new file in `pages/` (e.g., `pages/custom_report.py`)
2. Implement `render_custom_report()` function
3. Add to navigation in `components/sidebar.py`
4. Import and route in `app.py`

## 🔄 Workflow: Day 1 Setup

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Set API keys**: Copy `.env.example` to `.env` and fill your keys
3. **Configure Azure AD**: Add your Azure credentials to `.env`
4. **Run app**: `streamlit run app.py`
5. **Create use cases**: Go to Dashboard → Use Cases
6. **Monitor costs**: Check Cost Tracking page

## 📊 Data Flow

```
┌─────────────────────────────────────────────┐
│  Azure AD Authentication (auth/azure_sso.py) │
└──────────────────┬──────────────────────────┘
                   │
         ┌─────────▼──────────┐
         │   Sidebar (nav)   │
         └─────────┬──────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
┌───▼──────┐  ┌───▼──────┐  ┌───▼──────┐
│ Dashboard │  │   Pages  │  │Settings  │
└──────────┘  └──────────┘  └──────────┘
    │              │              │
    └──────────────┼──────────────┘
                   │
         ┌─────────▼───────────┐
         │  Mock Data / DB    │
         └────────────────────┘
```

## 🛠️ Development Tips

### Adding Metrics to Dashboard

```python
# In pages/dashboard.py
from utils.helpers import generate_metric_card_html

st.markdown(
    generate_metric_card_html(
        label="My Metric",
        value="42",
        delta="5% up",
        delta_up=True
    ),
    unsafe_allow_html=True
)
```

### Creating Charts

```python
# In pages/your_page.py
from utils.charts import style_figure
import plotly.express as px

fig = px.bar(data, x="Category", y="Value")
fig = style_figure(fig, height=300)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
```

### Checking User Roles

```python
from auth.azure_sso import get_sso_manager

sso = get_sso_manager()
user = sso.get_current_user()
roles = sso.get_user_roles(user.get("mail"))

if "Admin" in roles:
    # Show admin-only features
```

## 🔑 Environment Variables Reference

See [.env.example](.env.example) for complete list. Key ones:

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| OPENAI_API_KEY | No | "" | OpenAI API access |
| AZURE_CLIENT_ID | Yes* | "" | Azure AD app ID |
| AZURE_TENANT_ID | Yes* | "" | Azure AD tenant |
| AZURE_CLIENT_SECRET | Yes* | "" | Azure AD secret |
| GOOGLE_API_KEY | No | "" | Google Gemini access |
| ANTHROPIC_API_KEY | No | "" | Claude API access |

*Only for production deployment with real Azure AD SSO

## 📈 Production Checklist

- [ ] Set all environment variables securely
- [ ] Configure Azure AD with proper redirect URIs
- [ ] Enable HTTPS/TLS
- [ ] Set up secrets management (e.g., Azure Key Vault)
- [ ] Configure monitoring and logging
- [ ] Set up backup strategy for database
- [ ] Review and test access control
- [ ] Run security audit
- [ ] Set up CI/CD pipeline
- [ ] Document runbook for ops team

## 🐛 Troubleshooting

### Azure AD Login Issues
- Ensure Client ID and Tenant ID are correct
- Check that redirect URI exactly matches Azure app registration
- Verify client secret hasn't expired

### Missing API Keys
- Check .env file exists and is properly formatted
- Ensure keys are valid and have necessary permissions
- Verify keys aren't accidentally committed to git

### Performance Issues
- Check `CACHE_TIMEOUT_SECONDS` in config/settings.py
- Monitor database queries if using real DB
- Use st.cache_data decorator for expensive operations

## 📞 Support & Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Azure AD**: https://docs.microsoft.com/en-us/azure/active-directory/
- **OpenAI API**: https://platform.openai.com/docs
- **Anthropic Claude**: https://docs.anthropic.com

## 📄 License

[Your License Here]

---

**Last Updated**: April 6, 2026
**Version**: 2.0.0 (Modular Production Release)
