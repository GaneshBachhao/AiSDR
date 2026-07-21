from datetime import UTC, datetime
from uuid import UUID, uuid4

from ..exceptions.discovery_exception import DiscoveryException


class Organization:
    """
    Domain entity representing an organization undergoing AI discovery.
    """

    def __init__(
        self,
        name: str,
        industry: str,
        size: str,
        description: str | None = None,
    ):
        self._id: UUID = uuid4()

        self.name = name
        self.industry = industry
        self.size = size
        self.description = description

        self.created_at = datetime.now(UTC)
        self.updated_at = self.created_at

        self._validate()

    # -------------------------
    # Properties
    # -------------------------

    @property
    def id(self) -> UUID:
        return self._id

    # -------------------------
    # Domain Logic
    # -------------------------

    def update_details(
        self,
        name: str | None = None,
        industry: str | None = None,
        size: str | None = None,
        description: str | None = None,
    ):
        """
        Update organization information.
        """

        if name:
            self.name = name

        if industry:
            self.industry = industry

        if size:
            self.size = size

        if description:
            self.description = description

        self.updated_at = datetime.now(UTC)

        self._validate()

    # -------------------------
    # Validation
    # -------------------------

    def _validate(self):

        if not self.name:
            raise DiscoveryException(
                "Organization name cannot be empty"
            )

        if not self.industry:
            raise DiscoveryException(
                "Industry is required"
            )

        if not self.size:
            raise DiscoveryException(
                "Organization size is required"
            )

    # -------------------------
    # Representation
    # -------------------------

    def __repr__(self):
        return (
            f"Organization("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"industry='{self.industry}')"
        )