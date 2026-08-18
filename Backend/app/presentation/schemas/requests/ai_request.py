from pydantic import BaseModel, ConfigDict, Field


class AIRequestSchema(BaseModel):
    """
    AI request schema.
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    prompt: str = Field(
        ...,
        min_length=1,
        description="Prompt sent to the AI model.",
    )

    provider: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="AI provider name.",
    )

    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
    )

    max_tokens: int = Field(
        default=1024,
        ge=1,
    )
