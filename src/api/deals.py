"""
Deal pipeline API endpoints.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

router = APIRouter()


class DealCreate(BaseModel):
    name: str
    contact_id: str
    account_id: Optional[str] = None
    value: float
    currency: str = "USD"
    stage: str = "qualification"
    close_date: Optional[str] = None
    custom_fields: Dict[str, Any] = {}


class DealResponse(BaseModel):
    id: str
    name: str
    contact_id: str
    account_id: Optional[str]
    value: float
    currency: str
    stage: str
    probability: int
    close_date: Optional[str]
    created_at: datetime


@router.get("/", response_model=List[DealResponse])
async def list_deals(
    stage: Optional[str] = None,
    owner_id: Optional[str] = None,
    min_value: Optional[float] = None,
):
    """List deals with optional filtering."""
    return []


@router.post("/", response_model=DealResponse, status_code=status.HTTP_201_CREATED)
async def create_deal(deal: DealCreate):
    """Create a new deal."""
    return {
        "id": "deal_abc123",
        "name": deal.name,
        "contact_id": deal.contact_id,
        "account_id": deal.account_id,
        "value": deal.value,
        "currency": deal.currency,
        "stage": deal.stage,
        "probability": 20,
        "close_date": deal.close_date,
        "created_at": datetime.utcnow(),
    }


@router.put("/{deal_id}/stage")
async def update_deal_stage(deal_id: str, stage: str, notes: Optional[str] = None):
    """Update deal stage (pipeline progression)."""
    stage_probabilities = {
        "qualification": 20,
        "discovery": 40,
        "proposal": 60,
        "negotiation": 80,
        "closed_won": 100,
        "closed_lost": 0,
    }
    return {
        "deal_id": deal_id,
        "stage": stage,
        "probability": stage_probabilities.get(stage, 50),
        "updated_at": datetime.utcnow().isoformat(),
    }


@router.get("/pipeline")
async def get_pipeline_summary():
    """Get pipeline summary by stage."""
    return {
        "stages": [
            {"stage": "qualification", "count": 10, "value": 50000},
            {"stage": "discovery", "count": 8, "value": 120000},
            {"stage": "proposal", "count": 5, "value": 200000},
            {"stage": "negotiation", "count": 3, "value": 150000},
        ],
        "total_pipeline_value": 520000,
        "weighted_value": 260000,
    }


@router.get("/forecast")
async def get_revenue_forecast(period: str = "quarter"):
    """Get revenue forecast based on pipeline."""
    return {
        "period": period,
        "expected_revenue": 180000,
        "best_case": 320000,
        "worst_case": 80000,
        "closed_to_date": 45000,
    }


@router.get("/stale")
async def get_stale_deals(days_threshold: int = 14):
    """Get deals that haven't been updated recently (rot alerts)."""
    return {"stale_deals": [], "threshold_days": days_threshold}
