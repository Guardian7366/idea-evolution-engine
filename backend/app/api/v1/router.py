from fastapi import APIRouter, Depends

from app.api.security import enforce_rate_limit
from app.api.v1.endpoints import analysis, ideas, sessions, synthesis, versions

api_router = APIRouter(dependencies=[Depends(enforce_rate_limit)])

api_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
api_router.include_router(ideas.router, prefix="/ideas", tags=["ideas"])
api_router.include_router(versions.router, prefix="/versions", tags=["versions"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(synthesis.router, prefix="/synthesis", tags=["synthesis"])