"""
Gemini Client

Wrapper around Google's Gemini SDK.

Uses lazy imports so tests can import this module
without requiring the Gemini SDK.
"""

from typing import Any


class GeminiClient:
    """
    Client for Google Gemini.
    """

    def __init__(self) -> None:
        """
        Lazy-load the Gemini SDK.

        This avoids ModuleNotFoundError during
        pytest collection when the SDK is not
        installed.
        """

        try:
            import google.generativeai as genai

        except ImportError as ex:

            raise ImportError(
                "google-generativeai is not installed.\n"
                "Install it using:\n"
                "pip install google-generativeai"
            ) from ex

        self._genai = genai

        # ------------------------------------------------
        # Keep your existing configuration here
        # Example:
        #
        # self._genai.configure(
        #     api_key=settings.GEMINI_API_KEY
        # )
        #
        # self.model = self._genai.GenerativeModel(...)
        #
        # ------------------------------------------------

    # ----------------------------------------------------
    # KEEP ALL YOUR EXISTING METHODS
    # ----------------------------------------------------

    # Example:
    #
    # def generate(...):
    #
    #     response = self.model.generate_content(...)
    #
    #     return response.text