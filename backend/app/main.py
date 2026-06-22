"""Main FastAPI application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.config import get_settings
from app.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

settings = get_settings()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="DecentralThink Marketing Agency API",
    description="API for managing marketing strategies and agents",
    version="0.1.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "version": "0.1.0"}


@app.get("/health")
async def detailed_health():
    """Detailed health check"""
    return {
        "status": "ok",
        "environment": settings.environment,
        "debug": settings.debug
    }


# Exception handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "internal_server_error",
            "message": "An unexpected error occurred"
        }
    )


# Include routers (will be added in Sprint 1)
# from app.routes import auth, chat, strategy, agents, execution, stripe, analytics

# @app.include_router(auth.router, prefix=settings.api_v1_prefix + "/auth", tags=["auth"])
# @app.include_router(chat.router, prefix=settings.api_v1_prefix + "/chat", tags=["chat"])
# ... etc


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
