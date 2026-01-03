"""Core configuration."""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    app_env: str = "development"
    app_debug: bool = False
    app_secret_key: str = "change-me"
    
    database_url: str = "postgresql+asyncpg://localhost/crm_db"
    redis_url: str = "redis://localhost:6379/0"
    
    salesforce_username: str = ""
    salesforce_password: str = ""
    salesforce_security_token: str = ""
    
    hubspot_api_key: str = ""
    hubspot_portal_id: str = ""
    
    clearbit_api_key: str = ""
    
    sync_interval_seconds: int = 300
    sync_batch_size: int = 100
    conflict_resolution: str = "source_wins"
    
    lifecycle_automation_enabled: bool = True
    engagement_score_threshold_mql: int = 30
    engagement_score_threshold_sql: int = 60
    
    allowed_origins: List[str] = ["*"]
    
    class Config:
        env_file = ".env"


settings = Settings()
