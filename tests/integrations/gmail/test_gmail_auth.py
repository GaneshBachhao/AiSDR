"""
Tests for GmailAuth.
"""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from app.integrations.gmail.gmail_auth import (
    GmailAuth,
)

from app.integrations.gmail.gmail_exceptions import (
    GmailAuthenticationException,
)


def test_load_credentials_returns_none_when_token_missing(
    monkeypatch,
):

    auth = GmailAuth()

    monkeypatch.setattr(

        auth,

        "token_file",

        Path("missing.json"),
    )

    assert auth._load_credentials() is None


def test_authenticate_without_credentials_file(
    monkeypatch,
):

    auth = GmailAuth()

    monkeypatch.setattr(

        auth,

        "credentials_file",

        Path("missing.json"),
    )

    with pytest.raises(
        GmailAuthenticationException,
    ):

        auth._authenticate()


def test_save_credentials(
    tmp_path,
):

    auth = GmailAuth()

    auth.token_file = tmp_path / "token.json"

    credentials = MagicMock()

    credentials.to_json.return_value = "{}"

    auth._save_credentials(
        credentials,
    )

    assert auth.token_file.exists()