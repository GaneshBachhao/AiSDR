from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.models
from app.api.routes import lead_router
from app.core.config import settings
from app.core.logger import logger
from app.database.database import Base, engine



@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""

    logger.info("=" * 60)
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info("Initializing database...")

    Base.metadata.create_all(bind=engine)

    logger.info("Database initialized successfully.")
    logger.info("=" * 60)

    yield

    logger.info("Application stopped.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# Register API routes
app.include_router(lead_router)


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