from typing import Any


class ApiResponse:

    @staticmethod
    def success(
        data: Any = None,
        message: str = "Success"
    ):

        return {
            "success": True,
            "message": message,
            "data": data
        }

    @staticmethod
    def error(
        message: str,
        errors: list | None = None
    ):

        return {
            "success": False,
            "message": message,
            "errors": errors or []
        }