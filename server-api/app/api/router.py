from fastapi import APIRouter

from app.api.routes_health import router as health_router
from app.api.routes_repairs import router as repairs_router
from app.api.routes_returns import router as returns_router
from app.api.routes_shipments import router as shipments_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(shipments_router)
api_router.include_router(repairs_router)
api_router.include_router(returns_router)