"""
Lifecycle automation service.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from src.core.config import settings


class LifecycleStage(Enum):
    LEAD = "lead"
    MQL = "mql"
    SQL = "sql"
    OPPORTUNITY = "opportunity"
    CUSTOMER = "customer"
    ADVOCATE = "advocate"


@dataclass
class StageTransition:
    contact_id: str
    from_stage: LifecycleStage
    to_stage: LifecycleStage
    trigger: str
    timestamp: datetime


@dataclass
class StageConfig:
    stage: LifecycleStage
    next_stage: Optional[LifecycleStage]
    conditions: List[Dict[str, Any]]
    actions: List[Dict[str, Any]]


class LifecycleService:
    """Service for managing contact lifecycle automation."""
    
    def __init__(self):
        self.stage_configs: Dict[LifecycleStage, StageConfig] = {}
        self._configure_default_stages()
    
    def _configure_default_stages(self):
        """Configure default lifecycle stages."""
        self.stage_configs[LifecycleStage.LEAD] = StageConfig(
            stage=LifecycleStage.LEAD,
            next_stage=LifecycleStage.MQL,
            conditions=[
                {"field": "engagement_score", "operator": "gte", "value": settings.engagement_score_threshold_mql}
            ],
            actions=[
                {"type": "notify", "config": {"team": "marketing"}},
            ],
        )
        
        self.stage_configs[LifecycleStage.MQL] = StageConfig(
            stage=LifecycleStage.MQL,
            next_stage=LifecycleStage.SQL,
            conditions=[
                {"field": "meeting_scheduled", "operator": "eq", "value": True}
            ],
            actions=[
                {"type": "assign", "config": {"to": "sales_team"}},
                {"type": "notify", "config": {"team": "sales"}},
            ],
        )
        
        self.stage_configs[LifecycleStage.SQL] = StageConfig(
            stage=LifecycleStage.SQL,
            next_stage=LifecycleStage.OPPORTUNITY,
            conditions=[
                {"field": "budget_confirmed", "operator": "eq", "value": True}
            ],
            actions=[
                {"type": "create_deal", "config": {}},
            ],
        )
    
    async def evaluate_transition(
        self,
        contact_id: str,
        current_stage: LifecycleStage,
        contact_data: Dict[str, Any]
    ) -> Optional[StageTransition]:
        """
        Evaluate if contact should transition to next stage.
        
        Returns StageTransition if conditions are met, None otherwise.
        """
        if not settings.lifecycle_automation_enabled:
            return None
        
        config = self.stage_configs.get(current_stage)
        if not config or not config.next_stage:
            return None
        
        # Evaluate conditions
        all_conditions_met = True
        for condition in config.conditions:
            field = condition["field"]
            operator = condition["operator"]
            expected = condition["value"]
            actual = contact_data.get(field)
            
            if not self._evaluate_condition(actual, operator, expected):
                all_conditions_met = False
                break
        
        if all_conditions_met:
            return StageTransition(
                contact_id=contact_id,
                from_stage=current_stage,
                to_stage=config.next_stage,
                trigger=f"conditions_met:{config.conditions}",
                timestamp=datetime.utcnow(),
            )
        
        return None
    
    def _evaluate_condition(self, actual: Any, operator: str, expected: Any) -> bool:
        """Evaluate a single condition."""
        if operator == "eq":
            return actual == expected
        elif operator == "neq":
            return actual != expected
        elif operator == "gte":
            return actual is not None and actual >= expected
        elif operator == "gt":
            return actual is not None and actual > expected
        elif operator == "lte":
            return actual is not None and actual <= expected
        elif operator == "lt":
            return actual is not None and actual < expected
        return False
    
    async def execute_transition_actions(
        self,
        transition: StageTransition,
        config: StageConfig
    ) -> List[Dict[str, Any]]:
        """Execute actions associated with a stage transition."""
        results = []
        
        for action in config.actions:
            action_type = action["type"]
            action_config = action.get("config", {})
            
            # Execute action (placeholder)
            results.append({
                "action": action_type,
                "config": action_config,
                "executed": True,
            })
        
        return results


lifecycle_service = LifecycleService()
