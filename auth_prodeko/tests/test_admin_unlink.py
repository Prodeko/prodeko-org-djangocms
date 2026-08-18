"""Undoing a Keycloak link from the admin.

An account carries the subject of the Keycloak identity it belongs to,
and the sign-in path refuses any identity presenting a different one,
with a message telling whoever reads the log to resolve it by hand.
Deleting a Keycloak user and creating it again at the same address is
enough to reach that state, so the resolution has to be something an
administrator can actually perform.
"""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from auth_prodeko.oidc.backend import KeycloakOIDCBackend

User = get_user_model()


@pytest.fixture(autouse=True)
def _db(db):
    pass


@pytest.fixture
def admin_client(client):
    client.force_login(
        User.objects.create_superuser(email="root@prodeko.org", password=None)
    )
    return client


@pytest.fixture
def linked_account():
    return User.objects.create_user(
        email="maija@prodeko.org",
        keycloak_sub="the-deleted-keycloak-user",
        keycloak_linked_at=timezone.now(),
    )


def unlink(client, *accounts):
    return client.post(
        reverse("admin:auth_prodeko_user_changelist"),
        {
            "action": "unlink_from_keycloak",
            "_selected_action": [str(account.pk) for account in accounts],
        },
        follow=True,
    )


def test_unlinking_clears_the_subject_and_the_timestamp(admin_client, linked_account):
    response = unlink(admin_client, linked_account)

    assert response.status_code == 200
    linked_account.refresh_from_db()
    assert linked_account.keycloak_sub is None
    assert linked_account.keycloak_linked_at is None


def test_the_next_sign_in_links_the_account_afresh(
    admin_client, linked_account, settings
):
    """The point of the action: the member gets their account back by
    signing in, and keeps everything on it."""
    settings.OIDC_RP_CLIENT_ID = "prodekoorg"
    settings.OIDC_RP_CLIENT_SECRET = "secret"
    settings.OIDC_OP_TOKEN_ENDPOINT = "https://id.invalid/token"
    settings.OIDC_OP_USER_ENDPOINT = "https://id.invalid/userinfo"
    settings.OIDC_OP_JWKS_ENDPOINT = "https://id.invalid/certs"
    backend = KeycloakOIDCBackend()
    claims = {
        "sub": "the-recreated-keycloak-user",
        "email": "maija@prodeko.org",
        "email_verified": True,
        "given_name": "Maija",
        "family_name": "Meikalainen",
        "realm_access": {"roles": ["membership"]},
    }

    unlink(admin_client, linked_account)
    user = backend.update_user(backend.filter_users_by_claims(claims)[0], claims)

    assert user.pk == linked_account.pk
    assert user.keycloak_sub == "the-recreated-keycloak-user"


def test_unlinking_several_accounts_at_once_is_allowed(admin_client):
    """The subject column is unique, and clearing it leaves nulls, which
    postgres does not count as duplicates."""
    accounts = [
        User.objects.create_user(email=f"m{n}@prodeko.org", keycloak_sub=f"sub-{n}")
        for n in range(3)
    ]

    unlink(admin_client, *accounts)

    assert not User.objects.exclude(keycloak_sub=None).exists()


def test_the_subject_cannot_be_typed_in_by_hand(admin_client, linked_account):
    """Clearing it is the whole of the useful operation. Setting one by
    hand would hand another person's Keycloak identity this account."""
    url = reverse("admin:auth_prodeko_user_change", args=[linked_account.pk])

    response = admin_client.get(url)

    assert response.status_code == 200
    assert 'name="keycloak_sub"' not in response.content.decode()
