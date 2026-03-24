from fastapi import APIRouter

from app.api.v1.endpoints import ideas, sessions

api_v1_router = APIRouter()

# Register versioned endpoints here.
api_v1_router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])
api_v1_router.include_router(ideas.router, prefix="/ideas", tags=["ideas"])
