"""Main application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import contacts, deals, accounts, sync, lifecycle
from src.core.config import settings

app = FastAPI(
    title="CRM Automation System",
    description="End-to-end CRM automation with pipeline management and integrations",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contacts.router, prefix="/api/contacts", tags=["contacts"])
app.include_router(deals.router, prefix="/api/deals", tags=["deals"])
app.include_router(accounts.router, prefix="/api/accounts", tags=["accounts"])
app.include_router(sync.router, prefix="/api/sync", tags=["sync"])
app.include_router(lifecycle.router, prefix="/api/lifecycle", tags=["lifecycle"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
