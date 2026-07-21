from app.domain.discovery.entities.discovery_session import DiscoverySession


class DiscoveryService:
    """
    Domain service for Discovery business operations.
    """

    @staticmethod
    def start(session: DiscoverySession) -> None:
        """
        Start a discovery session.
        """
        session.start()

    @staticmethod
    def complete(
        session: DiscoverySession,
        summary: str | None = None,
    ) -> None:
        """
        Complete a discovery session.
        """
        session.complete(summary)