class TokenUsage:
    """
    Represents token consumption for an AI response.
    """

    def __init__(
        self,
        prompt_tokens: int,
        completion_tokens: int,
    ):
        if prompt_tokens < 0:
            raise ValueError(
                "Prompt tokens cannot be negative."
            )

        if completion_tokens < 0:
            raise ValueError(
                "Completion tokens cannot be negative."
            )

        self._prompt_tokens = prompt_tokens
        self._completion_tokens = completion_tokens

    @property
    def prompt_tokens(self):
        return self._prompt_tokens

    @property
    def completion_tokens(self):
        return self._completion_tokens

    @property
    def total_tokens(self):
        return (
            self.prompt_tokens +
            self.completion_tokens
        )

    def __eq__(self, other):
        return (
            isinstance(other, TokenUsage)
            and (
                self.prompt_tokens,
                self.completion_tokens,
            ) == (
                other.prompt_tokens,
                other.completion_tokens,
            )
        )

    def __hash__(self):
        return hash(
            (
                self.prompt_tokens,
                self.completion_tokens,
            )
        )