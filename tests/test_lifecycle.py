"""
Tests for lifecycle service.
"""

import pytest
from datetime import datetime
from src.services.lifecycle import (
    LifecycleService,
    LifecycleStage,
    StageTransition,
)


@pytest.fixture
def lifecycle_service():
    return LifecycleService()


class TestLifecycleService:
    
    @pytest.mark.asyncio
    async def test_evaluate_transition_lead_to_mql(self, lifecycle_service):
        """Test lead to MQL transition when engagement score threshold met."""
        contact_data = {
            "engagement_score": 35,
        }
        
        transition = await lifecycle_service.evaluate_transition(
            contact_id="con_123",
            current_stage=LifecycleStage.LEAD,
            contact_data=contact_data,
        )
        
        assert transition is not None
        assert transition.from_stage == LifecycleStage.LEAD
        assert transition.to_stage == LifecycleStage.MQL
    
    @pytest.mark.asyncio
    async def test_no_transition_below_threshold(self, lifecycle_service):
        """Test no transition when engagement score below threshold."""
        contact_data = {
            "engagement_score": 20,
        }
        
        transition = await lifecycle_service.evaluate_transition(
            contact_id="con_123",
            current_stage=LifecycleStage.LEAD,
            contact_data=contact_data,
        )
        
        assert transition is None
    
    @pytest.mark.asyncio
    async def test_evaluate_transition_mql_to_sql(self, lifecycle_service):
        """Test MQL to SQL transition when meeting scheduled."""
        contact_data = {
            "meeting_scheduled": True,
        }
        
        transition = await lifecycle_service.evaluate_transition(
            contact_id="con_123",
            current_stage=LifecycleStage.MQL,
            contact_data=contact_data,
        )
        
        assert transition is not None
        assert transition.from_stage == LifecycleStage.MQL
        assert transition.to_stage == LifecycleStage.SQL
    
    def test_evaluate_condition_eq(self, lifecycle_service):
        assert lifecycle_service._evaluate_condition(True, "eq", True) is True
        assert lifecycle_service._evaluate_condition(False, "eq", True) is False
    
    def test_evaluate_condition_gte(self, lifecycle_service):
        assert lifecycle_service._evaluate_condition(50, "gte", 30) is True
        assert lifecycle_service._evaluate_condition(30, "gte", 30) is True
        assert lifecycle_service._evaluate_condition(20, "gte", 30) is False
