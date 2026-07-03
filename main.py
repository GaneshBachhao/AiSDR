from fastapi import FastAPI

from app.core.config import settings

from app.core.logger import logger

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)


@app.on_event("startup")
def startup():

    logger.info("Application Started")


@app.get("/")
def home():

    return {

        "application": settings.APP_NAME,

        "version": settings.APP_VERSION,

        "environment": settings.ENVIRONMENT,

        "status": "Running"

    }


@app.get("/health")
def health():

    return {

        "status": "healthy"

    }