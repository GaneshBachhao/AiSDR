"""
Application Composition Root.

Responsible for constructing and wiring the
complete application dependency graph.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from app.application.ai.handlers.execute_ai_request_handler import (
    ExecuteAIRequestHandler,
)
from app.application.ai.services.ai_execution_service import (
    AIExecutionService,
)
from app.application.ai.validators.execute_ai_request_validator import (
    ExecuteAIRequestValidator,
)

from app.infrastructure.ai.adapters.application_ai_provider import (
    ApplicationAIProvider,
)

from app.infrastructure.ai.clients import (
    AzureOpenAIClient,
    GeminiClient,
    OllamaClient,
    OpenAIClient,
)

from app.infrastructure.ai.configuration import (
    ProviderSettings,
)

from app.infrastructure.ai.providers import (
    AzureOpenAIProvider,
    GeminiProvider,
    OllamaProvider,
    OpenAIProvider,
)

from app.infrastructure.persistence.database import (
    create_engine,
    create_session_factory,
)

from app.infrastructure.persistence.unit_of_work.sqlalchemy_unit_of_work import (
    SQLAlchemyUnitOfWork,
)


class Container:
    """
    Application Composition Root.
    """

    def __init__(
        self,
        connection_string: str,
        provider_settings: ProviderSettings,
    ) -> None:

        #
        # Database
        #

        self._engine = create_engine(
            connection_string,
        )

        self._session_factory: async_sessionmaker[
            AsyncSession
        ] = create_session_factory(
            self._engine,
        )

        #
        # Clients
        #

        openai_client = OpenAIClient(
            provider_settings,
        )

        azure_client = AzureOpenAIClient(
            provider_settings,
        )

        gemini_client = GeminiClient(
            provider_settings,
        )

        ollama_client = OllamaClient(
            provider_settings,
        )

        #
        # Providers
        #

        providers = {

            "openai": OpenAIProvider(
                openai_client,
                provider_settings,
            ),

            "azure_openai": AzureOpenAIProvider(
                azure_client,
                provider_settings,
            ),

            "gemini": GeminiProvider(
                gemini_client,
                provider_settings,
            ),

            "ollama": OllamaProvider(
                ollama_client,
                provider_settings,
            ),
        }

        self._application_provider = (
            ApplicationAIProvider(
                providers,
            )
        )

    #
    # Infrastructure
    #

    def unit_of_work(
        self,
    ) -> SQLAlchemyUnitOfWork:

        return SQLAlchemyUnitOfWork(
            self._session_factory,
        )

    #
    # Application
    #

    def ai_execution_service(
        self,
    ) -> AIExecutionService:

        return AIExecutionService(
            provider=self._application_provider,
        )

    #
    # Handlers
    #

    def execute_ai_request_handler(
        self,
    ) -> ExecuteAIRequestHandler:

        return ExecuteAIRequestHandler(
            service=self.ai_execution_service(),
            validator=ExecuteAIRequestValidator(),
        )