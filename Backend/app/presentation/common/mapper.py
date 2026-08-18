from typing import Any


class PresentationMapper:
    """
    Base presentation mapper.
    """

    @staticmethod
    def to_dict(obj: Any) -> dict:
        """
        Convert an object to a dictionary.
        """

        if hasattr(obj, "model_dump"):
            return obj.model_dump()

        if hasattr(obj, "__dict__"):
            return vars(obj)

        raise TypeError(f"Unsupported object type: {type(obj)}")
