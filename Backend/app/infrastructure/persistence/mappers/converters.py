"""
Registers all persistence converters.
"""

from __future__ import annotations

from app.domain.ai.value_objects.provider_name import ProviderName
from app.domain.lead.value_objects.lead_score import LeadScore
from app.domain.shared.identifiers.identifier import Identifier

from .converter_registry import converter_registry


#
# Generic Identifier converter
#
converter_registry.register(
    Identifier,
    to_database=lambda value: value.value,
    to_domain=lambda value: value,
)


#
# LeadScore
#
converter_registry.register(
    LeadScore,
    to_database=lambda value: value.value,
    to_domain=LeadScore,
)


#
# ProviderName
#
converter_registry.register(
    ProviderName,
    to_database=lambda value: value.value,
    to_domain=ProviderName,
)