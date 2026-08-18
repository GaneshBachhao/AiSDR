from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class StartDiscoveryRequest(BaseModel):
    """
    Start discovery request.
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    company_name: str = Field(
        ...,
        min_length=2,
        max_length=200,
    )

    website: HttpUrl
