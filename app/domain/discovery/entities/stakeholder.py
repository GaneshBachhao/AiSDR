from datetime import UTC, datetime
from uuid import UUID, uuid4

from ..exceptions.discovery_exception import DiscoveryException


class Stakeholder:
    """
    Domain entity representing a person involved in discovery.
    """

    def __init__(
        self,
        name: str,
        role: str,
        email: str,
        responsibility: str | None = None,
    ):
        self._id: UUID = uuid4()

        self.name = name
        self.role = role
        self.email = email
        self.responsibility = responsibility

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
    # Domain Behaviour
    # -------------------------

    def update_role(
        self,
        role: str,
        responsibility: str | None = None,
    ):
        """
        Update stakeholder responsibilities.
        """

        self.role = role

        if responsibility:
            self.responsibility = responsibility

        self.updated_at = datetime.now(UTC)

        self._validate()


    # -------------------------
    # Validation
    # -------------------------

    def _validate(self):

        if not self.name:
            raise DiscoveryException(
                "Stakeholder name cannot be empty"
            )

        if not self.role:
            raise DiscoveryException(
                "Stakeholder role is required"
            )

        if not self.email:
            raise DiscoveryException(
                "Stakeholder email is required"
            )


    # -------------------------
    # Representation
    # -------------------------

    def __repr__(self):

        return (
            f"Stakeholder("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"role='{self.role}')"
        )