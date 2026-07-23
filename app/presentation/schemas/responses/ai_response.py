from pydantic import BaseModel, ConfigDict


class AIResponseSchema(BaseModel):
    """
    AI response schema.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    content: str
    provider: str
    model: str

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

    finish_reason: str