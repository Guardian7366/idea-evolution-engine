from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_v1_router
from app.shared.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

# Configure frontend origins from environment-based settings.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, str]:
    """Simple root endpoint to confirm the API is running."""
    return {
        "message": f"{settings.app_name} is running",
        "environment": settings.app_env,
    }


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint for quick status verification."""
    return {
        "message": f"{settings.app_name} is healthy",
        "environment": settings.app_env,
    }


# Main versioned API router.
app.include_router(api_v1_router, prefix="/api/v1")
