"""
Account management API endpoints.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

router = APIRouter()


class AccountCreate(BaseModel):
    name: str
    domain: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None  # startup, smb, mid_market, enterprise
    annual_revenue: Optional[float] = None
    custom_fields: Dict[str, Any] = {}


class AccountResponse(BaseModel):
    id: str
    name: str
    domain: Optional[str]
    industry: Optional[str]
    size: Optional[str]
    health_score: int
    total_deal_value: float
    contact_count: int
    created_at: datetime


@router.get("/", response_model=List[AccountResponse])
async def list_accounts(
    industry: Optional[str] = None,
    size: Optional[str] = None,
):
    """List accounts with optional filtering."""
    return []


@router.post("/", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_account(account: AccountCreate):
    """Create a new account."""
    return {
        "id": "acc_abc123",
        "name": account.name,
        "domain": account.domain,
        "industry": account.industry,
        "size": account.size,
        "health_score": 75,
        "total_deal_value": 0,
        "contact_count": 0,
        "created_at": datetime.utcnow(),
    }


@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(account_id: str):
    """Get account by ID."""
    raise HTTPException(status_code=404, detail="Account not found")


@router.get("/{account_id}/contacts")
async def get_account_contacts(account_id: str):
    """Get all contacts for an account."""
    return {"account_id": account_id, "contacts": []}


@router.get("/{account_id}/deals")
async def get_account_deals(account_id: str):
    """Get all deals for an account."""
    return {"account_id": account_id, "deals": []}


@router.get("/{account_id}/health")
async def get_account_health(account_id: str):
    """Get account health metrics."""
    return {
        "account_id": account_id,
        "health_score": 75,
        "factors": [
            {"factor": "engagement", "score": 80, "trend": "up"},
            {"factor": "nps", "score": 70, "trend": "stable"},
            {"factor": "support_tickets", "score": 85, "trend": "up"},
            {"factor": "product_usage", "score": 65, "trend": "down"},
        ],
        "at_risk": False,
    }
