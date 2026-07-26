from app.domain.shared.base import DomainEvent

from ..value_objects.discovery_id import DiscoveryId


class DiscoveryStarted(DomainEvent):
    """
    Raised when discovery starts.
    """

    def __init__(self, discovery_id: DiscoveryId):
        super().__init__()
        self.discovery_id = discovery_id