from __future__ import annotations

from datetime import UTC, datetime, timedelta

import jwt
import pytest

from app.infrastructure.configuration.jwt_settings import JWTSettings
from app.infrastructure.security.jwt_service import JWTService


def _settings(**overrides) -> JWTSettings:
    defaults = {
        "jwt_secret_key": "test-secret",
        "jwt_algorithm": "HS256",
        "jwt_access_token_expire_minutes": 480,
    }
    defaults.update(overrides)
    return JWTSettings(**defaults)


def test_encode_then_decode_round_trips_the_subject() -> None:
    service = JWTService(_settings())

    token = service.encode(subject="user-123")
    payload = service.decode(token)

    assert payload["sub"] == "user-123"


def test_decode_raises_on_a_tampered_signature() -> None:
    service = JWTService(_settings())
    other_service = JWTService(_settings(jwt_secret_key="a-different-secret"))

    token = other_service.encode(subject="user-123")

    with pytest.raises(jwt.PyJWTError):
        service.decode(token)


def test_decode_raises_on_an_expired_token() -> None:
    service = JWTService(_settings())
    now = datetime.now(UTC)
    expired_token = jwt.encode(
        {"sub": "user-123", "iat": now - timedelta(hours=1), "exp": now - timedelta(minutes=1)},
        "test-secret",
        algorithm="HS256",
    )

    with pytest.raises(jwt.ExpiredSignatureError):
        service.decode(expired_token)
