from app.emails.providers.gmail_provider import (
    GmailProvider,
)

from app.emails.providers.provider_factory import (
    EmailProviderFactory,
)


def test_create_provider():

    provider = EmailProviderFactory.create()

    assert isinstance(
        provider,
        GmailProvider,
    )