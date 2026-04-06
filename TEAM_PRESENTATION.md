# 🚀 AI Platform Hub - Team Presentation Guide

**Version:** 2.0.0  
**Date:** April 2026  
**Status:** Production Ready with Demo Mode  

---

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [Project Overview](#project-overview)
3. [Architecture & Structure](#architecture--structure)
4. [Key Features](#key-features)
5. [Technology Stack](#technology-stack)
6. [Getting Started](#getting-started)
7. [User Guide](#user-guide)
8. [Complete File Structure](#complete-file-structure)
9. [How to Extend](#how-to-extend)
10. [Deployment Options](#deployment-options)
11. [Team Responsibilities](#team-responsibilities)
12. [Support & Troubleshooting](#support--troubleshooting)

---

## 🎯 Executive Summary

**AI Platform Hub** is an enterprise-grade web application for managing, monitoring, and optimizing AI use cases across multiple departments. It provides:

- **Real-time Analytics** - Usage metrics, cost tracking, performance monitoring
- **Use Case Management** - Create, manage, and track AI initiatives
- **Multi-Model Support** - GPT-4, Claude, Gemini, Mistral, Azure OpenAI
- **Role-Based Access** - Admin, AI Team, Department-level permissions
- **Enterprise Ready** - Azure SSO, secure API key management, audit trails

**Current Status:** ✅ Fully functional with demo data. Ready for Azure SSO configuration.

---

## 📖 Project Overview

### What is AI Platform Hub?

An all-in-one platform for organizations to:
- **Organize** AI projects by department and use case
- **Monitor** usage, costs, and performance in real-time
- **Control** access via role-based permissions
- **Scale** from teams to enterprise deployments
- **Integrate** with multiple LLM providers

### Why Was It Built?

**Problem:** Large organizations struggle to:
- Track AI spending across departments
- Manage permissions for AI resources
- Monitor model performance and costs
- Prevent duplicate efforts (same use case across departments)

**Solution:** A centralized hub with visibility, control, and insights.

### Who Uses It?

| Role | Access | Responsibilities |
|------|--------|-----------------|
| **Admin** | Full system | User management, configuration, billing |
| **AI Team Lead** | Analytics, cost tracking | Monitor usage, optimize models |
| **Department Manager** | Own department only | Manage use cases, budget |
| **End User** | Create use cases | Submit, monitor, provide feedback |

---

## 🏗️ Architecture & Structure

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     STREAMLIT FRONTEND                       │
│  (React-like components, responsive design, real-time UI)   │
└──────────────┬──────────────────────────────────────────────┘
               │
┌──────────────┴──────────────────────────────────────────────┐
│           APPLICATION LAYER (Python/Modular)                │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌────────────┐  ┌──────────┐  ┌──────────┐  │
│  │  Auth/   │  │  Business  │  │   Data   │  │   UI     │  │
│  │  SSO     │  │   Logic    │  │  Models  │  │ Components │ │
│  └──────────┘  └────────────┘  └──────────┘  └──────────┘  │
└──────────────┬──────────────────────────────────────────────┘
               │
┌──────────────┴──────────────────────────────────────────────┐
│         DATA LAYER (PostgreSQL / Mock Data)                  │
├─────────────────────────────────────────────────────────────┤
│  Use Cases │ Feedback │ Cost Logs │ Audit Trails │ Settings │
└─────────────────────────────────────────────────────────────┘
```

### Folder Structure

```
📦 oesl_ai_ui/
├── 📄 app.py                    ← Main router (entry point)
├── 📁 config/
│   └── 📄 settings.py           ← Centralized configuration
├── 📁 auth/
│   └── 📄 azure_sso.py          ← Authentication logic
├── 📁 pages/                    ← 11 Individual pages
│   ├── 📄 login.py              ← Authentication UI
│   ├── 📄 dashboard.py          ← KPI overview
│   ├── 📄 use_cases.py          ← Use case management
│   ├── 📄 models.py             ← LLM model info
│   ├── 📄 analytics.py          ← Usage analytics
│   ├── 📄 cost_tracking.py      ← Cost monitoring
│   ├── 📄 performance.py        ← Performance metrics
│   ├── 📄 notifications.py      ← System alerts
│   ├── 📄 settings.py           ← User preferences
│   ├── 📄 activity_log.py       ← Audit trail
│   ├── 📄 user_feedback.py      ← Feedback analytics
│   └── 📄 admin.py              ← Admin panel
├── 📁 components/
│   ├── 📄 sidebar.py            ← Navigation sidebar
│   ├── 📄 styles.py             ← Global CSS/theming
│   └── 📄 logo.py               ← SVG logos & icons
├── 📁 utils/
│   ├── 📄 helpers.py            ← Formatting, helpers
│   └── 📄 charts.py             ← Chart utilities
├── 📁 data/
│   ├── 📄 models.py             ← Data classes
│   └── 📄 mock_data.py          ← Test data generation
├── 📁 docs/
│   ├── 📄 README.md             ← Main documentation
│   ├── 📄 ADD_USECASE_GUIDE.md  ← Extension guide
│   ├── 📄 API_KEYS_GUIDE.md     ← API setup
│   └── 📄 DEPLOYMENT_GUIDE.md   ← Deployment options
├── 📄 requirements.txt           ← Dependencies
├── 📄 .env.example              ← Environment template
├── 📄 ARCHITECTURE.md           ← Technical details
└── 📄 QUICKSTART.md             ← Quick start guide
```

### Module Relationships

```
app.py (Main Router)
├── config.settings (Configuration)
├── auth.azure_sso (Authentication)
├── components.sidebar (Navigation)
├── components.styles (Theming)
├── data.mock_data (Demo Data)
└── pages/* (12 Page Components)
    ├── components/* (Reusable)
    ├── utils/* (Helpers)
    └── data/* (Models)
```

---

## ✨ Key Features

### 1. **Dashboard** 📊
- 4 KPI cards (Active Cases, Monthly Cost, API Calls, Success Rate)
- 3 analytical tabs (All Cases, By Department, Cost Analysis)
- Real-time metrics with trends

### 2. **Use Case Management** 📦
- Create, list, filter use cases
- Filter by status, department, type
- Track usage metrics per case
- Cost monitoring

### 3. **Analytics** 📈
- 30-day usage trends
- Performance metrics (response times, success rates)
- Model distribution analysis
- Historical data tracking

### 4. **Cost Tracking** 💰
- Monthly budget overview with progress
- Cost analysis by use case, department, model
- Cost trend predictions
- Alert thresholds

### 5. **Performance Monitoring** ⚡
- Response time analytics
- Error rate tracking
- Model-wise performance comparison
- SLA monitoring

### 6. **Multi-Model Support** 🤖
- OpenAI (GPT-4, GPT-4o, GPT-3.5)
- Anthropic Claude (3.5, 3, Haiku)
- Google Gemini
- Mistral AI
- Azure OpenAI (enterprise)

### 7. **User & Access Management** 👥
- Azure AD SSO integration
- Role-based access control
- Department-based permissions
- User activity tracking

### 8. **Audit & Compliance** 📋
- Complete activity logs
- User action tracking
- Change history
- Compliance reports

### 9. **Notifications** 🔔
- System alerts
- Budget alerts
- Performance warnings
- Activity notifications

### 10. **Settings Management** ⚙️
- User preferences
- Theme customization (dark/light)
- API key management
- Account settings

### 11. **Admin Panel** 🛡️
- System configuration
- User management
- Feature flags
- Documentation access

### 12. **User Feedback** 📝
- Feedback collection
- Rating analytics
- Use case reviews
- Performance insights

---

## 🛠️ Technology Stack

### Frontend
- **Streamlit 1.28.0+** - Web framework (Python)
- **Plotly 5.14.0** - Interactive charts & visualizations
- **Pandas 2.0.0** - Data manipulation
- **NumPy 1.24.0** - Numerical computing

### Backend
- **Python 3.8+** - Core language
- **Streamlit Sessions** - State management
- **Python Dataclasses** - Data models

### Authentication
- **MSAL 1.24+** - Microsoft Authentication Library
- **Azure AD** - Enterprise SSO
- **PKCE Flow** - Secure authentication

### Database (Production)
- **PostgreSQL 13+** - Primary database
- **SQLAlchemy** - ORM (optional)
- **Alembic** - Migrations (optional)

### Deployment
- **Streamlit Cloud** - Easiest (SaaS)
- **Docker** - Containerization
- **Heroku** - Platform as a Service
- **AWS ECS** - Enterprise
- **On-Premise** - Full control

### Development
- **Git** - Version control
- **pip** - Package management
- **Python virtual environments** - Isolation

---

## 🚀 Getting Started

### Step 1: Download & Setup

```bash
# Clone repository
git clone https://github.com/Dheeru66k/mock_ai_ui.git
cd mock_ai_ui

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

### Step 2: Run with Demo Account

```bash
streamlit run app.py
```

The app will:
- ✅ Auto-login with demo account
- ✅ Load mock data automatically
- ✅ Show dashboard with sample use cases
- ✅ Allow testing all features

**Demo Account:**
- **Email:** demo@aiplatform.local
- **Name:** Demo User
- **Department:** AI Team
- **Role:** AI Team + User

### Step 3: Access the App

Open your browser:
```
http://localhost:8501
```

You'll see:
1. Dashboard with 4 KPI cards
2. Sidebar with navigation
3. Mock data in all pages
4. Full feature access

---

## 📱 User Guide

### Dashboard Overview

The dashboard provides a quick snapshot:

| Card | Meaning |
|------|---------|
| **ACTIVE USE CASES** | Number of active AI projects |
| **MONTHLY COST (MTD)** | Cumulative LLM API costs this month |
| **TOTAL API CALLS** | Cumulative API calls made |
| **SUCCESS RATE** | Percentage of successful calls |

### Navigation

Use the **sidebar** to navigate:

```
┌─────────────────┐
│  MAIN SECTION   │
├─────────────────┤
│ 📊 Dashboard    │
│ 📦 Use Cases    │
├─────────────────┤
│ ANALYTICS       │
│ 📈 Analytics    │
│ 💰 Cost Tracking│
│ ⚡ Performance  │
├─────────────────┤
│ MANAGEMENT      │
│ 🤖 Models       │
│ 📋 Activity Log │
│ 👥 User Feedback│
├─────────────────┤
│ SYSTEM          │
│ 🔔 Notifications│
│ ⚙️ Settings     │
│ 🛡️ Admin Panel │
├─────────────────┤
│ 🌙 Theme Toggle │
│ Sign Out        │
└─────────────────┘
```

### Common Tasks

#### Task 1: View All Use Cases
1. Click **📦 Use Cases** in sidebar
2. See filtered list of all cases
3. Click any case for details
4. View metrics and costs

#### Task 2: Check Costs
1. Click **💰 Cost Tracking**
2. View monthly budget
3. See cost breakdown by use case/dept
4. Check cost trends

#### Task 3: Monitor Performance
1. Click **⚡ Performance**
2. View response times
3. Check error rates
4. Compare models

#### Task 4: Configure API Keys
1. Click **⚙️ Settings**
2. Scroll to "API Key Status"
3. Shows which keys are configured
4. To add: Update .env file

#### Task 5: View Audit Trail
1. Click **📋 Activity Log**
2. See all user actions
3. Filter by action, actor, date
4. Export for compliance

---

## 📁 Complete File Structure

### Core Application

**`app.py`** (127 lines)
- Main router
- Page navigation
- Authentication check
- Role-based access control

**`config/settings.py`** (170 lines)
- Azure AD configuration
- API key settings
- Business units
- Feature flags
- Color scheme

**`auth/azure_sso.py`** (220 lines)
- Azure authentication flow
- Token management
- User info retrieval
- Role mapping
- Demo user support

### Pages (11 files)

**`pages/login.py`** (100 lines)
- Azure SSO UI
- Demo login fallback
- "Sign in with Microsoft" button
- Decorative background

**`pages/dashboard.py`** (80 lines)
- 4 KPI metric cards
- 3 analytical tabs
- Trend arrows
- Use case table

**`pages/use_cases.py`** (60 lines)
- Use case listing
- Filtering (status, dept, type)
- Card-based display
- Click for details

**`pages/models.py`** (50 lines)
- Model comparison table
- Pricing info
- Context windows
- Setup instructions

**`pages/analytics.py`** (70 lines)
- Usage trends (30-day)
- Performance metrics
- Model distribution
- Historical data

**`pages/cost_tracking.py`** (110 lines)
- Budget progress bar
- 4 cost analyses
- Trend visualization
- Spending forecast

**`pages/performance.py`** (80 lines)
- Response time charts
- Success rate metrics
- Error distribution
- Model comparison

**`pages/notifications.py`** (40 lines)
- Alert listing
- Unread/all tabs
- Action buttons
- Type indicators

**`pages/settings.py`** (80 lines)
- Account information
- Theme toggle
- API key status
- Documentation links

**`pages/activity_log.py`** (50 lines)
- Audit trail
- Action filtering
- Date range selection
- Export option

**`pages/user_feedback.py`** (90 lines)
- Feedback summary
- Rating analytics
- Feedback by use case
- Individual entries

**`pages/admin.py`** (80 lines)
- System configuration
- User management
- Feature flags
- Documentation

### Components (3 files)

**`components/sidebar.py`** (120 lines)
- Navigation menu
- User info card
- Role-based nav sections
- Theme toggle
- Sign out button

**`components/styles.py`** (350 lines)
- Global CSS injection
- Dark/light theme
- Component styling
- Animations
- Responsive design

**`components/logo.py`** (200 lines)
- Hexagonal platform logo
- Use case type icons
- SVG generation
- Gradient styling

### Utilities (2 files)

**`utils/helpers.py`** (150 lines)
- Number formatting
- Currency formatting
- Percentage formatting
- Timestamps
- HTML generation
- Text manipulation

**`utils/charts.py`** (180 lines)
- Chart theming
- Color schemes
- Plotly factories
- Figure styling
- Layout utilities

### Data (2 files)

**`data/models.py`** (140 lines)
- LLMModel dataclass
- 7 available models
- Helper functions
- Provider grouping

**`data/mock_data.py`** (250 lines)
- Use case generator
- Time series data
- Feedback generator
- Audit log generator
- Notification generator

### Documentation (5 files)

**`docs/README.md`** (350 lines)
- Feature overview
- Quick start
- Customization guide
- Troubleshooting

**`docs/ADD_USECASE_GUIDE.md`** (450 lines)
- Step-by-step guide
- Code examples
- Integration examples
- Real-world examples

**`docs/API_KEYS_GUIDE.md`** (600 lines)
- 5 provider setups
- Cost breakdown
- Testing instructions
- Troubleshooting

**`docs/DEPLOYMENT_GUIDE.md`** (700 lines)
- 4 deployment options
- Step-by-step setup
- Configuration examples
- Cost estimates

**`QUICKSTART.md`** (350 lines)
- 3-step setup
- Next steps
- Documentation index
- Support info

### Configuration (3 files)

**`requirements.txt`**
- 20 Python packages
- Pinned versions
- Dependency list

**`.env.example`**
- Azure AD variables
- API key templates
- Feature flags
- Database config

**`ARCHITECTURE.md`**
- System design
- Component diagram
- Database schema
- Testing checklist

---

## 🎨 How to Extend

### Adding a New Use Case Type

1. **Update the data model:**
   ```python
   # data/models.py
   USE_CASE_TYPES = [
       "Content Generation",
       "Text Analysis",
       "Your New Type"  # Add here
   ]
   ```

2. **Generate test data:**
   ```python
   # data/mock_data.py
   def generate_mock_use_cases():
       use_cases.append({
           "type": "Your New Type",
           "description": "Description",
           ...
       })
   ```

3. **Update the use case page (optional):**
   ```python
   # pages/use_cases.py
   # Add filtering for new type
   types_filter = st.multiselect(
       "Type",
       options=["All Types", "Content Generation", "Your New Type"]
   )
   ```

### Adding a New Department

1. **Update config:**
   ```python
   # config/settings.py
   BUSINESS_UNITS: List[str] = [
       "Marketing",
       "Operations",
       "Your Department"  # Add here
   ]
   ```

2. **Test with mock data:**
   - Run app, mock data will include new department

### Adding a New Page

1. **Create the page file:**
   ```python
   # pages/your_page.py
   def render_your_page():
       st.markdown('<div class="section-header">📊 Your Page</div>', unsafe_allow_html=True)
       # Your page content
   ```

2. **Add to router:**
   ```python
   # app.py - Import
   from pages.your_page import render_your_page
   
   # Add to routes
   page_routes = {
       ...
       "your_page": render_your_page,
   }
   ```

3. **Add to sidebar:**
   ```python
   # components/sidebar.py
   nav_btn("🎯", "Your Page", "your_page")
   ```

### Adding a New LLM Provider

1. **Update data:**
   ```python
   # data/models.py
   AVAILABLE_MODELS.append({
       "id": "provider-model-1",
       "name": "Model Name",
       "provider": "Your Provider",
       "cost_per_1k_input": 0.0005,
       "cost_per_1k_output": 0.0015,
       "context_window": 4096,
       ...
   })
   ```

2. **Add API key:**
   ```bash
   # .env
   YOUR_PROVIDER_API_KEY=your_key_here
   ```

3. **Update API guide:**
   - Document in `docs/API_KEYS_GUIDE.md`

---

## 🌍 Deployment Options

### Option 1: Streamlit Cloud (Easiest)
- **Cost:** $5-10/month per app
- **Setup time:** 5 minutes
- **Scaling:** Automatic
- **Best for:** Teams < 50 people

### Option 2: Docker + Heroku
- **Cost:** $7-50/month
- **Setup time:** 30 minutes
- **Scaling:** Manual
- **Best for:** Teams 50-200

### Option 3: AWS ECS
- **Cost:** $20-100/month
- **Setup time:** 2-4 hours
- **Scaling:** Auto-scaling available
- **Best for:** Enterprise (200+)

### Option 4: On-Premise
- **Cost:** Infrastructure only
- **Setup time:** 4-8 hours
- **Scaling:** Manual
- **Best for:** Maximum control, compliance

**See `docs/DEPLOYMENT_GUIDE.md` for detailed steps.**

---

## 👥 Team Responsibilities

### Backend/DevOps Team
- [ ] Set up Azure AD application
- [ ] Configure API keys for LLM providers
- [ ] Set up PostgreSQL database
- [ ] Deploy to production environment
- [ ] Monitor application health
- [ ] Manage backups and recovery

### Frontend Team
- [ ] Customize branding/colors
- [ ] Add organization-specific pages
- [ ] Improve UI/UX based on feedback
- [ ] Implement additional visualizations
- [ ] Performance optimization

### Data Team
- [ ] Set up data pipeline to real database
- [ ] Create analytics dashboards
- [ ] Generate reports
- [ ] Data validation and quality checks
- [ ] Cost optimization analysis

### Product/Business Team
- [ ] Define use cases and departments
- [ ] Set up role structure
- [ ] Configure feature flags
- [ ] Plan roadmap
- [ ] Gather user feedback

### Security Team
- [ ] Azure AD configuration
- [ ] API key rotation policy
- [ ] Audit logging setup
- [ ] Compliance checks (GDPR, SOC2)
- [ ] Penetration testing

---

## 🆘 Support & Troubleshooting

### Common Issues

**Issue:** Sidebar not visible
- **Fix:** Ensure `ENABLE_MOCK_DATA=true` in config
- **Alternative:** Check browser console for errors

**Issue:** Demo account not auto-logging in
- **Fix:** Clear browser cache and refresh
- **Alternative:** Manually enter demo@aiplatform.local

**Issue:** Charts not loading
- **Fix:** Check Plotly installation: `pip install plotly`
- **Alternative:** Restart Streamlit app

**Issue:** "Module not found" error
- **Fix:** Run: `pip install -r requirements.txt`
- **Then:** Restart Streamlit

**Issue:** Azure SSO login fails
- **Fix:** Check `.env` for correct credentials
- **Alternative:** Use demo mode instead

### Getting Help

1. **Check Docs:** Start with `docs/README.md`
2. **Review Logs:** Check terminal output for errors
3. **Test Locally:** Use demo mode to isolate issues
4. **Contact DevOps:** For deployment issues
5. **GitHub Issues:** Report bugs on GitHub

### Performance Tips

- Use demo mode for testing
- Cache large datasets
- Limit chart data points to 100
- Use pagination for large lists
- Clear old mock data regularly

---

## 📚 Additional Resources

| Resource | Location | Content |
|----------|----------|---------|
| **Quick Start** | `QUICKSTART.md` | 3-step setup |
| **Main Docs** | `docs/README.md` | Features & customization |
| **Use Case Guide** | `docs/ADD_USECASE_GUIDE.md` | Extend functionality |
| **API Guide** | `docs/API_KEYS_GUIDE.md` | Integration setup |
| **Deployment** | `docs/DEPLOYMENT_GUIDE.md` | Production setup |
| **Architecture** | `ARCHITECTURE.md` | Technical details |
| **GitHub** | https://github.com/Dheeru66k/mock_ai_ui | Source code |

---

## 🎯 Next Steps

1. ✅ **Setup:** Follow QUICKSTART.md (5 minutes)
2. ✅ **Explore:** Click through all pages with demo data
3. ✅ **Customize:** Update config for your organization
4. ✅ **Integrate:** Add Azure AD or database
5. ✅ **Deploy:** Choose deployment option from guide
6. ✅ **Train:** Share this guide with your team
7. ✅ **Extend:** Add custom pages/features as needed

---

## 📞 Contact & Support

- **GitHub Repository:** https://github.com/Dheeru66k/mock_ai_ui
- **Issues:** Create GitHub issues for bugs
- **Discussions:** Share ideas and feedback
- **Documentation:** Comprehensive guides included

---

**Last Updated:** April 2026  
**Version:** 2.0.0  
**Status:** ✅ Production Ready

---

### Quick Command Reference

```bash
# Setup
git clone https://github.com/Dheeru66k/mock_ai_ui.git
cd mock_ai_ui
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Run
streamlit run app.py

# Push updates
git add -A
git commit -m "Your message"
git push origin main

# Install dependencies
pip install -r requirements.txt

# Clear cache
streamlit cache clear

# Run in production
streamlit run app.py --logger.level=error
```

