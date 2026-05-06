from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.v1.router import api_router
from app.infrastructure.persistence.database import Base, engine
from app.infrastructure.persistence.models.analysis_model import (
    VersionAnalysisModel,
    VersionComparisonModel,
)
from app.infrastructure.persistence.models.idea_model import IdeaModel
from app.infrastructure.persistence.models.session_model import SessionModel
from app.infrastructure.persistence.models.synthesis_model import FinalSynthesisModel
from app.infrastructure.persistence.models.version_model import IdeaVariantModel, IdeaVersionModel
from app.shared.config import settings
from app.shared.errors.domain_errors import DomainError
from app.shared.errors.infrastructure_errors import (
    AIProviderConfigurationError,
    InfrastructureError,
    OllamaConnectionError,
)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(), payment=()"
        )

        if not settings.app_debug:
            response.headers["Content-Security-Policy"] = (
                "default-src 'none'; "
                "frame-ancestors 'none'; "
                "base-uri 'none'; "
                "object-src 'none'"
            )

        return response

def create_application() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        debug=settings.app_debug,
        version="0.1.0",
    )

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.trusted_hosts,
    )

    if settings.security_headers_enabled:
        app.add_middleware(SecurityHeadersMiddleware)

    Base.metadata.create_all(bind=engine)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.backend_cors_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
    )

    @app.exception_handler(DomainError)
    async def handle_domain_error(_: Request, exc: DomainError):
        message = exc.message.lower()

        status_code = 400
        if "not found" in message:
            status_code = 404

        return JSONResponse(
            status_code=status_code,
            content={
                "error": {
                    "type": exc.__class__.__name__,
                    "message": exc.message,
                }
            },
        )

    @app.exception_handler(AIProviderConfigurationError)
    async def handle_ai_provider_configuration_error(
        _: Request,
        exc: AIProviderConfigurationError,
    ):
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "type": exc.__class__.__name__,
                    "message": exc.message,
                }
            },
        )

    @app.exception_handler(OllamaConnectionError)
    async def handle_ollama_connection_error(_: Request, exc: OllamaConnectionError):
        return JSONResponse(
            status_code=503,
            content={
                "error": {
                    "type": exc.__class__.__name__,
                    "message": exc.message,
                }
            },
        )

    @app.exception_handler(InfrastructureError)
    async def handle_infrastructure_error(_: Request, exc: InfrastructureError):
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "type": exc.__class__.__name__,
                    "message": exc.message,
                }
            },
        )

    @app.get("/", tags=["root"])
    def root():
        return {
            "message": "Idea Evolution Engine API is running.",
            "environment": settings.app_env,
            "api_prefix": settings.api_v1_prefix,
        }

    @app.get("/health", tags=["health"])
    def health():
        return {
            "status": "ok",
            "service": settings.app_name,
        }

    app.include_router(api_router, prefix=settings.api_v1_prefix)

    return app


app = create_application()