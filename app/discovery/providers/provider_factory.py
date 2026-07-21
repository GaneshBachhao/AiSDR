from app.core.config import settings

from app.discovery.providers.base_provider import (
    BaseDiscoveryProvider,
)

from app.discovery.providers.mock_provider import (
    MockDiscoveryProvider,
)

from app.lead_intelligence.providers.search_provider import (
    SearchProvider,
)

from app.exceptions.custom_exceptions import (
    UnsupportedDiscoveryProviderException,
)

from app.core.logger import logger


class DiscoveryProviderFactory:
    """
    Factory responsible for returning the configured
    Discovery Provider implementation.
    """

    _providers = {

        "mock": MockDiscoveryProvider,

        "search": SearchProvider,

    }

    @classmethod
    def get_provider(cls) -> BaseDiscoveryProvider:

        provider_name = settings.DISCOVERY_PROVIDER.lower()

        provider_class = cls._providers.get(
            provider_name,
        )

        if not provider_class:

            raise UnsupportedDiscoveryProviderException(
                provider_name,
            )

        logger.info(
            f"Using Discovery Provider: {provider_name}"
        )

        return provider_class()