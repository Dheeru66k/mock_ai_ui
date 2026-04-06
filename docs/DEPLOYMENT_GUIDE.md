# Production Deployment Guide

This guide covers deploying the AI Platform Hub to a production environment.

## Prerequisites

- Python 3.8+
- PostgreSQL 13+ (or your preferred database)
- Azure AD tenant configured
- Domain/SSL certificate
- Server with at least 2GB RAM
- Docker (optional but recommended)

## Deployment Options

### Option 1: Streamlit Cloud (Easiest)

Best for: Teams < 50 users, non-sensitive data

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Create Streamlit Cloud account**: https://share.streamlit.io

3. **Deploy**:
   - Click "New app"
   - Connect GitHub repo
   - Set Python version: 3.10
   - Set secrets (GitHub Settings → Actions secrets)

4. **Set Secrets in Streamlit Cloud**:
   ```
   OPENAI_API_KEY=sk-proj-...
   ANTHROPIC_API_KEY=sk-ant-...
   AZURE_CLIENT_ID=...
   AZURE_CLIENT_SECRET=...
   AZURE_TENANT_ID=...
   DATABASE_URL=postgresql://...
   ```

5. **Update Azure AD redirect URI**:
   ```
   https://your-app-name.streamlit.app/auth/callback
   ```

### Option 2: Docker + Heroku (Recommended for Small Teams)

1. **Create Dockerfile**:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. **Create .dockerignore**:

```
.git
.gitignore
.env
__pycache__
*.pyc
.pytest_cache
.venv
venv/
```

3. **Deploy to Heroku**:

```bash
# Install Heroku CLI
curl https://cli.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set OPENAI_API_KEY=sk-proj-...
heroku config:set AZURE_CLIENT_SECRET=...
heroku config:set DATABASE_URL=postgresql://...

# Build and deploy
git push heroku main

# View logs
heroku logs --tail
```

### Option 3: AWS + Docker (Recommended for Enterprise)

1. **Push image to ECR**:

```bash
# Create ECR repo
aws ecr create-repository --repository-name oesl-ai-ui --region us-east-1

# Authenticate
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin [ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com

# Build and push
docker build -t oesl-ai-ui:latest .
docker tag oesl-ai-ui:latest [ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com/oesl-ai-ui:latest
docker push [ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com/oesl-ai-ui:latest
```

2. **Deploy to ECS**:

Create task definition JSON, then:

```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
aws ecs create-service --cluster production --service-name oesl-ai-ui --task-definition oesl-ai-ui --desired-count 2
```

3. **Use RDS for Database**:

```bash
# Create RDS instance
aws rds create-db-instance \
  --db-instance-identifier oesl-ai-ui-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password [PASSWORD] \
  --allocated-storage 20
```

### Option 4: On-Premise with Nginx + Supervisor

1. **Install dependencies**:

```bash
sudo apt-get update
sudo apt-get install -y python3.10 python3-pip nginx supervisor postgresql

# Clone repo
git clone your-repo.git /opt/oesl-ai-ui
cd /opt/oesl-ai-ui
pip install -r requirements.txt
```

2. **Create Supervisor config**:

```ini
# /etc/supervisor/conf.d/oesl-ai-ui.conf
[program:oesl-ai-ui]
directory=/opt/oesl-ai-ui
command=/usr/bin/python3 -m streamlit run app.py --server.port 8501
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/oesl-ai-ui.log
environment=PATH="/opt/oesl-ai-ui/.venv/bin",OPENAI_API_KEY="sk-proj-...",AZURE_CLIENT_SECRET="..."
```

3. **Configure Nginx**:

```nginx
# /etc/nginx/sites-available/oesl-ai-ui
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /etc/ssl/certs/your-cert.crt;
    ssl_certificate_key /etc/ssl/private/your-key.key;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        
        # WebSocket support
        proxy_buffering off;
    }
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/oesl-ai-ui /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Database Migration

### From Mock Data to PostgreSQL

1. **Create schema**:

```sql
CREATE TABLE use_cases (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    owner VARCHAR(255),
    business_unit VARCHAR(100),
    type VARCHAR(100),
    status VARCHAR(50),
    model VARCHAR(100),
    monthly_cost DECIMAL(10, 2),
    usage_count INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE use_case_feedback (
    id SERIAL PRIMARY KEY,
    use_case_id VARCHAR(50) REFERENCES use_cases(id),
    rating INTEGER,
    comment TEXT,
    user_email VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE cost_logs (
    id SERIAL PRIMARY KEY,
    use_case_id VARCHAR(50) REFERENCES use_cases(id),
    cost DECIMAL(10, 4),
    tokens INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

2. **Migrate data**:

```python
# migrate_to_db.py
import psycopg2
from data.mock_data import generate_all_mock_data

def migrate_mock_data():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()
    
    mock_data = generate_all_mock_data()
    
    for uc in mock_data["use_cases"]:
        cur.execute("""
            INSERT INTO use_cases 
            (id, name, description, owner, business_unit, type, status, model, monthly_cost, usage_count)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            uc["id"], uc["name"], uc["description"],
            uc["owner"], uc["business_unit"], uc["type"],
            uc["status"], uc["model"],
            uc["monthly_cost"], uc["usage_count"]
        ))
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    migrate_mock_data()
    print("Migration complete!")
```

Run:
```bash
python migrate_to_db.py
```

## Monitoring & Logging

### Using Azure Monitor

```python
# config/logging_config.py
from applicationinsights import TelemetryClient
import os

app_insights_key = os.getenv("APPINSIGHTS_INSTRUMENTATION_KEY")
tc = TelemetryClient(app_insights_key)

def log_event(event_name: str, properties: dict = None):
    """Log event to Azure Monitor"""
    tc.track_event(event_name, properties)

def log_exception(exception: Exception):
    """Log exception to Azure Monitor"""
    tc.track_exception()
```

### Using ELK Stack

```yaml
# docker-compose.yml
version: '3'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.14.0
    environment:
      - discovery.type=single-node
    ports:
      - "9200:9200"
  
  kibana:
    image: docker.elastic.co/kibana/kibana:7.14.0
    ports:
      - "5601:5601"
  
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - ELASTICSEARCH_HOST=elasticsearch:9200
```

## Performance Optimization

### 1. Caching

```python
# In pages/dashboard.py
import streamlit as st

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_use_cases_from_db():
    # Expensive database query
    return use_cases
```

### 2. Database Indexing

```sql
CREATE INDEX idx_status ON use_cases(status);
CREATE INDEX idx_unit ON use_cases(business_unit);
CREATE INDEX idx_created ON use_cases(created_at DESC);
```

### 3. Load Balancing

For multiple app instances behind a load balancer:

```nginx
upstream streamlit_backend {
    server app1.internal:8501;
    server app2.internal:8501;
    server app3.internal:8501;
}

server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://streamlit_backend;
    }
}
```

## Backup & Disaster Recovery

### Database Backup

```bash
# Automated daily backup
0 2 * * * pg_dump $DATABASE_URL | gzip > /backups/oesl_ai_ui_$(date +\%Y\%m\%d).sql.gz

# Keep 30 days of backups
find /backups -name "oesl_ai_ui_*.sql.gz" -mtime +30 -delete
```

### Restore from Backup

```bash
gunzip < /backups/oesl_ai_ui_20240101.sql.gz | psql $DATABASE_URL
```

## Security Hardening

### SSL/TLS

```bash
# Using Let's Encrypt
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com
```

### Rate Limiting

```nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

server {
    location / {
        limit_req zone=api_limit burst=20 nodelay;
        proxy_pass http://localhost:8501;
    }
}
```

### Security Headers

```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https:" always;
```

## Monitoring Checklist

- [ ] Application logs being collected
- [ ] Database backups automated and tested
- [ ] Uptime monitoring configured
- [ ] Alert thresholds set for:
  - High error rates
  - Slow response times
  - Database connection issues
  - API quota exhaustion
- [ ] Performance baselines established
- [ ] Load testing completed

## Post-Deployment

1. Run smoke tests against production
2. Monitor error rates for first 24 hours
3. Set up on-call rotation
4. Document runbooks for common issues
5. Plan scaling strategy

## Troubleshooting

### App crashes on startup
```bash
streamlit run app.py --logger.level=debug
```

### Out of memory
- Reduce `CACHE_TIMEOUT_SECONDS`
- Lower `ITEMS_PER_PAGE`
- Switch to PostgreSQL (if using SQLite)

### Slow page loads
- Check database indexes
- Enable browser caching
- Consider CDN for static assets

See [README.md](README.md) for more info.
