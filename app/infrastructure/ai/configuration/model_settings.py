"""
AI model configuration.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ModelSettings:
    """
    Configuration describing a single AI model.
    """

    model_name: str

    max_tokens: int = 4096

    temperature: float = 0.7

    supports_streaming: bool = False

    context_window: int = 8192

    capabilities: list[str] = field(
        default_factory=list,
    )

    def __post_init__(self) -> None:

        model = self.model_name.strip()

        if not model:
            raise ValueError(
                "Model name is required."
            )

        object.__setattr__(
            self,
            "model_name",
            model,
        )

        if self.max_tokens <= 0:
            raise ValueError(
                "Max tokens must be greater than zero."
            )

        if not (
            0.0 <= self.temperature <= 2.0
        ):
            raise ValueError(
                "Temperature must be between 0 and 2."
            )

        if self.context_window <= 0:
            raise ValueError(
                "Context window must be greater than zero."
            )

    def supports(
        self,
        capability: str,
    ) -> bool:
        return (
            capability.lower()
            in {
                c.lower()
                for c in self.capabilities
            }
        )

    def supports_capability(self, capability: str) -> bool:
        """Return whether the model exposes the requested capability."""
        return self.supports(capability)
