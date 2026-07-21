from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.common.response import ApiResponse
from app.exceptions.custom_exceptions import (
    AgneticAIException,
    LeadNotFoundException,
    DuplicateLeadException,
)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(LeadNotFoundException)
    async def lead_not_found_handler(
        request: Request,
        exc: LeadNotFoundException,
    ):
        return JSONResponse(
            status_code=404,
            content=ApiResponse.error(exc.message),
        )

    @app.exception_handler(DuplicateLeadException)
    async def duplicate_lead_handler(
        request: Request,
        exc: DuplicateLeadException,
    ):
        return JSONResponse(
            status_code=409,
            content=ApiResponse.error(exc.message),
        )

    @app.exception_handler(AgneticAIException)
    async def generic_handler(
        request: Request,
        exc: AgneticAIException,
    ):
        return JSONResponse(
            status_code=400,
            content=ApiResponse.error(exc.message),
        )