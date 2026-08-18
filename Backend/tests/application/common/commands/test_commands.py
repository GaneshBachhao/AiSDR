# tests/application/common/commands/test_commands.py

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.application.common.commands import (
    Command,
    CommandHandler,
)


class CreateTestCommand(Command):
    """
    Test command.
    """

    name: str


class TestCommandHandler(
    CommandHandler[
        CreateTestCommand,
        str,
    ],
):
    """
    Test command handler.
    """

    async def handle(
        self,
        command: CreateTestCommand,
    ) -> str:
        return command.name


def test_command_accepts_valid_data() -> None:
    command = CreateTestCommand(
        name="Pamacore",
    )

    assert command.name == "Pamacore"


def test_command_is_immutable() -> None:
    command = CreateTestCommand(
        name="Initial",
    )

    with pytest.raises(ValidationError):
        command.name = "Changed"


def test_command_rejects_unknown_fields() -> None:
    with pytest.raises(ValidationError):
        CreateTestCommand(
            name="Test",
            invalid="value",
        )


@pytest.mark.asyncio
async def test_command_handler_executes() -> None:
    handler = TestCommandHandler()

    result = await handler.handle(
        CreateTestCommand(
            name="Pamacore",
        ),
    )

    assert result == "Pamacore"
