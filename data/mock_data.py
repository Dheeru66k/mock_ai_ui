"""
Mock Data Generation
Generates realistic demo data for dashboard and testing.
Used when ENABLE_MOCK_DATA=True in config.
"""

import random
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any


def generate_mock_use_cases() -> List[Dict]:
    """Generate mock use case data
    
    Returns:
        List of mock use case dictionaries
    """
    random.seed(42)
    np.random.seed(42)
    
    now = datetime.now()
    
    use_cases = [
        # Marketing Department Use Cases
        {
            "id": "uc-001",
            "name": "Campaign Copy Generator",
            "description": "Generates marketing copy variants for campaigns across email, social, and display channels.",
            "owner": "sarah.chen@company.com",
            "owner_name": "Sarah Chen",
            "business_unit": "Marketing",
            "type": "Content Generation",
            "status": "active",
            "model": "claude-3-5-sonnet",
            "created": now - timedelta(days=120),
            "last_accessed": now - timedelta(hours=2),
            "usage_count": 3847,
            "monthly_cost": 284.50,
            "avg_response_ms": 1230,
            "success_rate": 98.2,
            "users": ["marketing-team", "agency-partners"],
            "tags": ["marketing", "copywriting"],
            "params": {
                "temperature": 0.8,
                "max_tokens": 1024,
                "top_p": 0.95,
                "frequency_penalty": 0.3,
                "presence_penalty": 0.1,
            },
        },
        {
            "id": "uc-002",
            "name": "Customer Sentiment Analyzer",
            "description": "Analyzes customer feedback from surveys, reviews, and support tickets for sentiment and themes.",
            "owner": "sarah.chen@company.com",
            "owner_name": "Sarah Chen",
            "business_unit": "Marketing",
            "type": "Text Analysis",
            "status": "active",
            "model": "gpt-4o-mini",
            "created": now - timedelta(days=85),
            "last_accessed": now - timedelta(hours=5),
            "usage_count": 12540,
            "monthly_cost": 178.20,
            "avg_response_ms": 680,
            "success_rate": 99.1,
            "users": ["cx-team", "marketing-team", "product-team"],
            "tags": ["sentiment", "analytics"],
            "params": {
                "temperature": 0.2,
                "max_tokens": 512,
                "top_p": 0.9,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0,
            },
        },
        # Operations Department Use Cases
        {
            "id": "uc-004",
            "name": "Incident Report Summarizer",
            "description": "Condenses verbose incident reports into executive summaries with action items and risk scores.",
            "owner": "james.wright@company.com",
            "owner_name": "James Wright",
            "business_unit": "Operations",
            "type": "Summarization",
            "status": "active",
            "model": "claude-3-haiku",
            "created": now - timedelta(days=200),
            "last_accessed": now - timedelta(minutes=45),
            "usage_count": 8920,
            "monthly_cost": 95.40,
            "avg_response_ms": 540,
            "success_rate": 99.6,
            "users": ["ops-team", "executives", "risk-team"],
            "tags": ["operations", "reporting"],
            "params": {
                "temperature": 0.1,
                "max_tokens": 800,
                "top_p": 0.85,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0,
            },
        },
        {
            "id": "uc-005",
            "name": "Supplier Contract Reviewer",
            "description": "Reviews supplier contracts to flag non-standard clauses, risk terms, and compliance issues.",
            "owner": "james.wright@company.com",
            "owner_name": "James Wright",
            "business_unit": "Operations",
            "type": "Document Review",
            "status": "active",
            "model": "gemini-1-5-pro",
            "created": now - timedelta(days=60),
            "last_accessed": now - timedelta(hours=1),
            "usage_count": 1230,
            "monthly_cost": 310.60,
            "avg_response_ms": 3200,
            "success_rate": 97.8,
            "users": ["legal-team", "procurement-team"],
            "tags": ["legal", "contracts"],
            "params": {
                "temperature": 0.1,
                "max_tokens": 4096,
                "top_p": 0.9,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0,
            },
        },
        # Finance Department Use Cases
        {
            "id": "uc-007",
            "name": "Financial Report Narrator",
            "description": "Transforms raw financial tables into natural language narratives for board presentations.",
            "owner": "priya.patel@company.com",
            "owner_name": "Priya Patel",
            "business_unit": "Finance",
            "type": "Report Generation",
            "status": "active",
            "model": "claude-3-5-sonnet",
            "created": now - timedelta(days=95),
            "last_accessed": now - timedelta(hours=3),
            "usage_count": 678,
            "monthly_cost": 140.30,
            "avg_response_ms": 1890,
            "success_rate": 98.8,
            "users": ["finance-team", "executives"],
            "tags": ["finance", "reporting"],
            "params": {
                "temperature": 0.4,
                "max_tokens": 2000,
                "top_p": 0.92,
                "frequency_penalty": 0.1,
                "presence_penalty": 0.1,
            },
        },
        {
            "id": "uc-008",
            "name": "Expense Anomaly Detector",
            "description": "Flags unusual expense patterns, duplicate submissions, and policy violations automatically.",
            "owner": "priya.patel@company.com",
            "owner_name": "Priya Patel",
            "business_unit": "Finance",
            "type": "Anomaly Detection",
            "status": "active",
            "model": "gpt-4o-mini",
            "created": now - timedelta(days=45),
            "last_accessed": now,
            "usage_count": 24500,
            "monthly_cost": 220.50,
            "avg_response_ms": 490,
            "success_rate": 99.3,
            "users": ["finance-team", "hr-team", "audit-team"],
            "tags": ["finance", "compliance"],
            "params": {
                "temperature": 0.0,
                "max_tokens": 256,
                "top_p": 1.0,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0,
            },
        },
    ]
    
    return use_cases


def generate_mock_time_series(use_cases: List[Dict]) -> tuple:
    """Generate usage time series data
    
    Args:
        use_cases: List of use cases
        
    Returns:
        Tuple of (dates, usage_series, cost_series)
    """
    now = datetime.now()
    days = 90
    dates = [now - timedelta(days=i) for i in range(days, 0, -1)]
    
    usage_series = {}
    cost_series = {}
    
    for uc in use_cases:
        base = uc["usage_count"] / 90
        noise = np.random.normal(0, base * 0.3, days)
        trend = np.linspace(-base * 0.2, base * 0.2, days)
        vals = np.clip(base + noise + trend, 0, None).astype(int)
        
        usage_series[uc["id"]] = vals.tolist()
        cost_series[uc["id"]] = (
            vals * (uc["monthly_cost"] / max(uc["usage_count"], 1))
        ).tolist()
    
    return dates, usage_series, cost_series


def generate_mock_notifications() -> List[Dict]:
    """Generate mock notifications"""
    now = datetime.now()
    return [
        {
            "id": "n-1",
            "type": "warn",
            "title": "High Usage Alert",
            "msg": "uc-005 (Supplier Contract Reviewer) usage is 150% above normal.",
            "time": now - timedelta(hours=1),
            "read": False,
        },
        {
            "id": "n-2",
            "type": "info",
            "title": "New Model Available",
            "msg": "GPT-4 Turbo has been added to available models.",
            "time": now - timedelta(hours=6),
            "read": False,
        },
        {
            "id": "n-3",
            "type": "success",
            "title": "Cost Optimization",
            "msg": "Your use case uc-002 is optimized. Could save $45/month.",
            "time": now - timedelta(days=1),
            "read": True,
        },
    ]


def generate_mock_feedback() -> List[Dict]:
    """Generate mock user feedback"""
    now = datetime.now()
    use_case_ids = ["uc-001", "uc-002", "uc-004", "uc-005", "uc-007", "uc-008"]
    use_case_names = {
        "uc-001": "Campaign Copy Generator",
        "uc-002": "Customer Sentiment Analyzer",
        "uc-004": "Incident Report Summarizer",
        "uc-005": "Supplier Contract Reviewer",
        "uc-007": "Financial Report Narrator",
        "uc-008": "Expense Anomaly Detector",
    }
    
    comments = [
        "Really helpful, saved me hours on campaigns!",
        "Output quality is consistently excellent.",
        "Sometimes too verbose, but generally good.",
        "Fast and reliable service.",
        "Could improve accuracy on edge cases.",
        "Great integration with our workflows.",
    ]
    
    feedback = []
    for i in range(15):
        uc_id = random.choice(use_case_ids)
        feedback.append({
            "id": f"fb-{i+1:03d}",
            "uc_id": uc_id,
            "uc_name": use_case_names[uc_id],
            "rating": random.choice([3, 4, 4, 5, 5]),
            "comment": random.choice(comments),
            "user_email": f"user{random.randint(1,20)}@company.com",
            "time": now - timedelta(days=random.randint(0, 30)),
        })
    
    return feedback


def generate_mock_audit_log() -> List[Dict]:
    """Generate mock audit log entries"""
    now = datetime.now()
    actions = [
        ("UseCase Created", "Campaign strategies use case created", "uc-001"),
        ("Model Changed", "Updated to GPT-4o", "uc-002"),
        ("Parameters Updated", "Adjusted temperature to 0.2", "uc-004"),
        ("Status Changed", "Marked as inactive", "uc-006"),
        ("Cost Optimization", "Applied cost-saving parameters", "uc-008"),
    ]
    
    audit = []
    for i, (action, detail, uc_id) in enumerate(actions):
        audit.append({
            "id": f"audit-{i+1:03d}",
            "timestamp": now - timedelta(hours=i*4 + random.randint(0, 3)),
            "actor": f"user{random.randint(1,5)}@company.com",
            "action": action,
            "detail": detail,
            "uc_id": uc_id,
        })
    
    return audit


def generate_all_mock_data() -> Dict[str, Any]:
    """Generate all mock data
    
    Returns:
        Dictionary containing all mock data
    """
    use_cases = generate_mock_use_cases()
    dates, usage_series, cost_series = generate_mock_time_series(use_cases)
    
    return {
        "use_cases": use_cases,
        "dates": dates,
        "usage_series": usage_series,
        "cost_series": cost_series,
        "notifications": generate_mock_notifications(),
        "feedback": generate_mock_feedback(),
        "audit": generate_mock_audit_log(),
    }
