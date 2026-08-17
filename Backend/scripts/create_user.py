"""
Create (or update the password of) an operator-provisioned login user.

There is no self-service registration in this app -- accounts are
provisioned by a human operator running this script directly against the
real database.

Usage (from Backend/, with the venv active -- run as a module, not a
bare script path, so the `app` package resolves on sys.path):

    python -m scripts.create_user --email admin@example.com
    python -m scripts.create_user --email admin@example.com --password "..."
    python -m scripts.create_user --email admin@example.com --update-password

If --password is omitted, the password is prompted for via getpass so it
never lands in shell history. Re-running for an email that already exists
does nothing unless --update-password is passed -- an accidental re-run
must not silently rotate an existing account's password.
"""

from __future__ import annotations

import argparse
import asyncio
import getpass

from app.domain.user.entities.user import User
from app.domain.user.value_objects.email import Email
from app.domain.user.value_objects.password_hash import PasswordHash
from app.infrastructure.configuration.database_settings import DatabaseSettings
from app.infrastructure.persistence.database.session import get_session_manager
from app.infrastructure.persistence.unit_of_work.sqlalchemy_unit_of_work import (
    SqlAlchemyUnitOfWork,
)
from app.infrastructure.security.password_hasher import PasswordHasher


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", default=None)
    parser.add_argument(
        "--update-password",
        action="store_true",
        help="If the email already exists, update its password instead of leaving it untouched.",
    )
    return parser.parse_args()


async def main() -> None:
    args = _parse_args()

    password = args.password or getpass.getpass("Password: ")
    if not password:
        raise SystemExit("A non-empty password is required.")

    email = Email(args.email)
    hasher = PasswordHasher()

    settings = DatabaseSettings()
    manager = get_session_manager(settings)
    session = manager.create_session()

    try:
        uow = SqlAlchemyUnitOfWork(session=session)

        async with uow:
            existing = await uow.user_repository.find_by_email(email.value)

            if existing is not None:
                if not args.update_password:
                    print(
                        f"User {email.value} already exists (id={existing.id.value}). "
                        "Pass --update-password to change it."
                    )
                    return

                existing.change_password(PasswordHash(hasher.hash(password)))
                await uow.user_repository.update(existing)
                await uow.commit()
                print(f"Updated password for {email.value} (id={existing.id.value}).")
                return

            user = User(
                email=email,
                password_hash=PasswordHash(hasher.hash(password)),
            )
            await uow.user_repository.add(user)
            await uow.commit()
            print(f"Created user {email.value} (id={user.id.value}).")
    finally:
        await session.close()


if __name__ == "__main__":
    asyncio.run(main())
