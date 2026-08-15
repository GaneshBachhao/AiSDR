# tests/application/common/behaviors/test_behaviors.py

from __future__ import annotations

import pytest

from app.application.common.behaviors import (
    Pipeline,
)


@pytest.mark.asyncio
async def test_pipeline_executes_handler() -> None:

    pipeline = Pipeline(
        behaviors=[],
    )

    async def handler(
        request: str,
    ) -> str:

        return request.upper()

    result = await pipeline.execute(
        "pamacore",
        handler,
    )

    assert result == "PAMACORE"


@pytest.mark.asyncio
async def test_pipeline_executes_behavior_order() -> None:

    calls: list[str] = []

    class SampleBehavior:

        async def handle(
            self,
            request: str,
            next_handler,
        ) -> str:

            calls.append("before")

            result = await next_handler(
                request,
            )

            calls.append("after")

            return result


    pipeline = Pipeline(
        behaviors=[
            SampleBehavior(),
        ],
    )

    async def handler(
        request: str,
    ) -> str:

        calls.append("handler")

        return request


    result = await pipeline.execute(
        "test",
        handler,
    )

    assert result == "test"
    assert calls == [
        "before",
        "handler",
        "after",
    ]