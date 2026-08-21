from __future__ import annotations

import pytest

from app.domain.sequence.enums.touch_channel import TouchChannel
from app.domain.sequence.value_objects.touch import Touch


def test_accepts_a_valid_touch() -> None:
    touch = Touch(channel=TouchChannel.EMAIL, wait_days=3)

    assert touch.channel is TouchChannel.EMAIL
    assert touch.wait_days == 3


def test_rejects_negative_wait_days() -> None:
    with pytest.raises(ValueError, match="wait_days cannot be negative"):
        Touch(channel=TouchChannel.EMAIL, wait_days=-1)


def test_allows_zero_wait_days() -> None:
    touch = Touch(channel=TouchChannel.EMAIL, wait_days=0)

    assert touch.wait_days == 0


def test_content_defaults_to_none() -> None:
    touch = Touch(channel=TouchChannel.EMAIL, wait_days=0)

    assert touch.content is None


def test_accepts_content() -> None:
    touch = Touch(channel=TouchChannel.EMAIL, wait_days=0, content="Hi there...")

    assert touch.content == "Hi there..."
