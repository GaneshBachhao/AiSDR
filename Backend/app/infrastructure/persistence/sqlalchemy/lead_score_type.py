"""
LeadScore SQLAlchemy TypeDecorator.
"""

from sqlalchemy import Integer

from app.domain.lead.value_objects.lead_score import LeadScore
from app.infrastructure.persistence.sqlalchemy.type_decorators import (
    ValueObjectType,
)


class LeadScoreType(ValueObjectType[LeadScore]):
    """
    LeadScore <-> INTEGER
    """

    impl = Integer

    value_object = LeadScore