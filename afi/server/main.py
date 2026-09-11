"""FastAPI application server.

Main API gateway and orchestrator.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from config.settings import get_settings

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure FastAPI application.
    
    Returns:
        Configured FastAPI app
    """
    settings = get_settings()
    
    app = FastAPI(
        title="Arabic Financial Intelligence Platform",
        description="Production-grade AI-powered financial advisor for Arabic speakers",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins.split(","),
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {
            "status": "healthy",
            "version": "0.1.0",
            "ai_provider": settings.ai_provider,
        }
    
    # API routes will be added here
    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "message": "مرحبا بك في منصة الذكاء المالي العربية",
            "status": "ready",
        }
    
    return app


if __name__ == "__main__":
    import uvicorn
    
    settings = get_settings()
    app = create_app()
    
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
    )
