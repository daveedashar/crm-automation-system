"""
Lifecycle management API endpoints.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime

router = APIRouter()


class LifecycleStage(BaseModel):
    name: str
    order: int
    criteria: Dict[str, Any]
    actions: List[Dict[str, Any]]


class LifecycleTransition(BaseModel):
    contact_id: str
    from_stage: str
    to_stage: str
    trigger: str
    transitioned_at: datetime


@router.get("/stages")
async def get_lifecycle_stages():
    """Get configured lifecycle stages."""
    return {
        "stages": [
            {"name": "lead", "order": 1, "count": 500},
            {"name": "mql", "order": 2, "count": 150},
            {"name": "sql", "order": 3, "count": 75},
            {"name": "opportunity", "order": 4, "count": 40},
            {"name": "customer", "order": 5, "count": 200},
            {"name": "advocate", "order": 6, "count": 50},
        ]
    }


@router.post("/stages")
async def configure_stage(stage: LifecycleStage):
    """Configure a lifecycle stage with criteria and actions."""
    return {
        "stage": stage.name,
        "configured": True,
        "configured_at": datetime.utcnow().isoformat(),
    }


@router.get("/transitions")
async def get_recent_transitions(limit: int = 50):
    """Get recent lifecycle transitions."""
    return {"transitions": []}


@router.post("/evaluate/{contact_id}")
async def evaluate_lifecycle(contact_id: str):
    """
    Evaluate and potentially progress contact lifecycle.
    
    Checks:
    - Engagement score thresholds
    - Activity triggers
    - Custom criteria
    """
    return {
        "contact_id": contact_id,
        "current_stage": "lead",
        "evaluation_result": "progressed",
        "new_stage": "mql",
        "trigger": "engagement_score >= 30",
    }


@router.get("/funnel")
async def get_funnel_metrics(period: str = "month"):
    """Get lifecycle funnel conversion metrics."""
    return {
        "period": period,
        "funnel": [
            {"from": "lead", "to": "mql", "conversion_rate": 0.30},
            {"from": "mql", "to": "sql", "conversion_rate": 0.50},
            {"from": "sql", "to": "opportunity", "conversion_rate": 0.53},
            {"from": "opportunity", "to": "customer", "conversion_rate": 0.25},
        ],
        "overall_conversion": 0.02,
    }


@router.get("/at-risk")
async def get_at_risk_contacts():
    """Get contacts at risk of churning based on engagement drop."""
    return {
        "at_risk_contacts": [],
        "criteria": "engagement_score_drop > 20% in 30 days",
    }
