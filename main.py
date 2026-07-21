from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.models

from app.api.routes import lead_router
from app.api.routes.ai_router import router as ai_router

from app.core.config import settings
from app.core.logger import logger

from app.database.database import Base, engine

from app.exceptions import register_exception_handlers

from app.middleware.logging_middleware import LoggingMiddleware

from app.api.routes.discovery_router import router as discovery_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown events.
    """

    logger.info("=" * 60)
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment : {settings.ENVIRONMENT}")
    logger.info("Initializing database...")

    Base.metadata.create_all(bind=engine)

    logger.info("Database initialized successfully.")
    logger.info("=" * 60)

    yield

    logger.info("=" * 60)
    logger.info(f"Stopping {settings.APP_NAME}")
    logger.info("=" * 60)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# Register Global Exception Handlers
register_exception_handlers(app)

app.add_middleware(LoggingMiddleware)

# Register API Routers
app.include_router(lead_router)
app.include_router(ai_router)
app.include_router(discovery_router)

@app.get("/", tags=["Home"])
def home():
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "Running",
    }


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "healthy",
    }