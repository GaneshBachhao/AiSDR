from app.discovery.providers.provider_factory import DiscoveryProviderFactory

provider = DiscoveryProviderFactory.get_provider()

print(type(provider).__name__)