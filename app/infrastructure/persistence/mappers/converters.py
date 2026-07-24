"""
Registers all persistence converters.
"""

from app.domain.ai.value_objects.provider_name import ProviderName
from app.domain.common.value_objects.email_address import EmailAddress
from app.domain.common.value_objects.website_url import WebsiteUrl
from app.domain.lead.value_objects.lead_score import LeadScore

from .converter_registry import converter_registry


converter_registry.register(
    LeadScore,
    to_database=lambda value: value.value,
    to_domain=LeadScore,
)

converter_registry.register(
    EmailAddress,
    to_database=lambda value: value.value,
    to_domain=EmailAddress,
)

converter_registry.register(
    WebsiteUrl,
    to_database=lambda value: value.value,
    to_domain=WebsiteUrl,
)

converter_registry.register(
    ProviderName,
    to_database=lambda value: value.value,
    to_domain=ProviderName,
)