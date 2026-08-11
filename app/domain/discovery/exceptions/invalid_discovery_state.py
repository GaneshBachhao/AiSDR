from .discovery_exception import DiscoveryException


class InvalidDiscoveryState(DiscoveryException):
    """
    Raised when an invalid discovery state transition is attempted.
    """

    pass