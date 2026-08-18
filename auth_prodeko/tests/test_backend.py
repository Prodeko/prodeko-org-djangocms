import mozilla_django_oidc.auth
import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import SuspiciousOperation

from auth_prodeko.oidc.backend import KeycloakOIDCBackend

User = get_user_model()


@pytest.fixture(autouse=True)
def _db(db):
    pass


@pytest.fixture
def backend(settings):
    # The library's __init__ insists on these; nothing here contacts them.
    settings.OIDC_RP_CLIENT_ID = "prodekoorg"
    settings.OIDC_RP_CLIENT_SECRET = "secret"
    settings.OIDC_OP_TOKEN_ENDPOINT = "https://id.invalid/token"
    settings.OIDC_OP_USER_ENDPOINT = "https://id.invalid/userinfo"
    settings.OIDC_OP_JWKS_ENDPOINT = "https://id.invalid/certs"
    return KeycloakOIDCBackend()


def claims(**overrides):
    base = {
        "sub": "sub-1",
        "email": "maija@prodeko.org",
        "email_verified": True,
        "given_name": "Maija",
        "family_name": "Meikalainen",
        "realm_access": {"roles": ["membership"]},
    }
    base.update(overrides)
    return base


# --- verify_claims -------------------------------------------------------


def test_member_is_allowed(backend):
    assert backend.verify_claims(claims()) is True


def test_unverified_email_is_refused(backend):
    assert backend.verify_claims(claims(email_verified=False)) is False


def test_non_member_is_refused(backend):
    """Keycloak allows self-registration, so a bare account is not enough."""
    assert backend.verify_claims(claims(realm_access={"roles": []})) is False


def test_the_alumni_role_is_enough_on_its_own(backend):
    assert backend.verify_claims(claims(realm_access={"roles": ["alumni"]})) is True


def test_an_account_from_before_the_migration_needs_no_role(backend):
    """Nothing on prodeko.org has ever checked membership status, so a
    former member can sign in today. The role must not take that away."""
    User.objects.create_user(email="maija@prodeko.org", predates_keycloak=True)

    assert backend.verify_claims(claims(realm_access={"roles": []})) is True


def test_a_grandfathered_account_still_signs_in_once_linked(backend):
    """Every login after the first resolves by subject, not by address."""
    User.objects.create_user(
        email="maija@prodeko.org", keycloak_sub="sub-1", predates_keycloak=True
    )

    assert backend.verify_claims(claims(realm_access={"roles": []})) is True


def test_an_account_created_after_the_migration_still_needs_a_role(backend):
    """The cutoff is the point: whoever joins now and lapses later is
    refused, where whoever joined before the migration is not."""
    User.objects.create_user(email="maija@prodeko.org", keycloak_sub="sub-1")

    assert backend.verify_claims(claims(realm_access={"roles": []})) is False


def test_the_break_glass_address_grandfathers_nobody(backend, settings):
    """It holds the only password left, so registering its address at
    Keycloak must buy nothing at all."""
    settings.KEYCLOAK_BREAK_GLASS_EMAIL = "maija@prodeko.org"
    User.objects.create_user(email="maija@prodeko.org", predates_keycloak=True)

    assert backend.verify_claims(claims(realm_access={"roles": []})) is False


def test_an_address_claimed_by_another_subject_grandfathers_nobody(backend):
    """The row cannot be adopted, so it cannot vouch for the identity
    either; otherwise registering a member's old address would be enough."""
    User.objects.create_user(
        email="maija@prodeko.org", keycloak_sub="someone-else", predates_keycloak=True
    )

    assert backend.verify_claims(claims(realm_access={"roles": []})) is False


def test_malformed_token_is_refused_not_raised(backend):
    assert backend.verify_claims(claims(sub="")) is False


# --- resolution ----------------------------------------------------------


def test_links_existing_row_by_email(backend):
    legacy = User.objects.create_user(
        email="maija@prodeko.org", first_name="Vanha", last_name="Nimi"
    )
    user = backend.update_user(backend.filter_users_by_claims(claims())[0], claims())
    assert user.pk == legacy.pk
    assert user.keycloak_sub == "sub-1"
    assert user.keycloak_linked_at is not None


def test_email_match_is_case_insensitive(backend):
    legacy = User.objects.create_user(email="Maija@Prodeko.ORG")
    assert backend.filter_users_by_claims(claims())[0].pk == legacy.pk


def test_subject_match_wins_over_email(backend):
    linked = User.objects.create_user(
        email="old-address@prodeko.org", keycloak_sub="sub-1"
    )
    User.objects.create_user(email="maija@prodeko.org")
    assert backend.filter_users_by_claims(claims())[0].pk == linked.pk


def test_row_linked_to_another_subject_is_not_adopted(backend):
    User.objects.create_user(email="maija@prodeko.org", keycloak_sub="someone-else")
    with pytest.raises(SuspiciousOperation):
        backend.filter_users_by_claims(claims())


def test_break_glass_account_is_never_adopted(backend, settings):
    settings.KEYCLOAK_BREAK_GLASS_EMAIL = "maija@prodeko.org"
    User.objects.create_user(email="maija@prodeko.org")
    with pytest.raises(SuspiciousOperation):
        backend.filter_users_by_claims(claims())


def test_creates_a_user_when_nothing_matches(backend):
    user = backend.create_user(claims())
    assert user.email == "maija@prodeko.org"
    assert user.first_name == "Maija"
    assert user.keycloak_sub == "sub-1"
    assert not user.has_usable_password()


# --- the library's path after an empty filter -----------------------------
#
# mozilla_django_oidc reads an empty filter result as "create this user",
# which the unique constraint on email turns into a 500. These drive
# get_or_create_user, the real caller, with the userinfo request stubbed
# out so that nothing contacts Keycloak.


def resolve(backend, monkeypatch, payload):
    monkeypatch.setattr(backend, "get_userinfo", lambda *args: payload)
    return backend.get_or_create_user("access-token", "id-token", {})


def test_login_is_refused_when_the_address_belongs_to_another_subject(
    backend, monkeypatch
):
    User.objects.create_user(email="maija@prodeko.org", keycloak_sub="someone-else")
    with pytest.raises(SuspiciousOperation):
        resolve(backend, monkeypatch, claims())
    assert User.objects.count() == 1


def test_login_is_refused_for_the_break_glass_address(backend, settings, monkeypatch):
    settings.KEYCLOAK_BREAK_GLASS_EMAIL = "maija@prodeko.org"
    User.objects.create_user(email="maija@prodeko.org")
    with pytest.raises(SuspiciousOperation):
        resolve(backend, monkeypatch, claims())
    assert User.objects.count() == 1


def test_an_unknown_address_is_still_created(backend, monkeypatch):
    """The refusal must not fire when the address is simply new."""
    user = resolve(backend, monkeypatch, claims())
    assert user.email == "maija@prodeko.org"
    assert user.keycloak_sub == "sub-1"


# --- claims come from the ID token as well as UserInfo --------------------
#
# The library hands verify_claims whatever get_userinfo returns, and the
# realm-role mapper the setup guide specifies writes realm_access.roles to
# the ID token, not necessarily to UserInfo. These stub the one HTTP call
# the library makes, so nothing contacts Keycloak.


@pytest.fixture
def userinfo(monkeypatch):
    """Stub the UserInfo request and return a setter for its body."""

    body = {}

    class Response:
        headers = {"content-type": "application/json"}

        def raise_for_status(self):
            pass

        def json(self):
            return body

    monkeypatch.setattr(
        mozilla_django_oidc.auth.requests, "get", lambda *args, **kwargs: Response()
    )

    def respond_with(**claims):
        body.clear()
        body.update(claims)

    return respond_with


def test_roles_from_the_id_token_survive_a_userinfo_without_them(backend, userinfo):
    userinfo(sub="sub-1", email="maija@prodeko.org", email_verified=True)
    merged = backend.get_userinfo("access-token", "id-token", claims())
    assert merged["realm_access"] == {"roles": ["membership"]}


def test_userinfo_wins_where_both_define_a_claim(backend, userinfo):
    userinfo(sub="sub-1", email="uusi@prodeko.org")
    merged = backend.get_userinfo("access-token", "id-token", claims())
    assert merged["email"] == "uusi@prodeko.org"


@pytest.mark.parametrize("payload", [None, {}])
def test_a_missing_or_empty_payload_does_not_break_the_merge(
    backend, userinfo, payload
):
    userinfo(**claims())
    merged = backend.get_userinfo("access-token", "id-token", payload)
    assert merged == claims()


def test_a_member_known_only_to_the_id_token_may_sign_in(backend, userinfo):
    """The real path: verify_claims must see the ID token's roles."""
    userinfo(sub="sub-1", email="maija@prodeko.org", email_verified=True)
    user = backend.get_or_create_user("access-token", "id-token", claims())
    assert user.email == "maija@prodeko.org"
    assert user.keycloak_sub == "sub-1"


# --- privilege synchronisation -------------------------------------------


def test_admin_role_grants_staff(backend):
    user = backend.create_user(
        claims(realm_access={"roles": ["membership", "prodeko-org-admin"]})
    )
    assert user.is_staff is True
    assert user.is_superuser is False


def test_superuser_role_grants_both(backend):
    user = backend.create_user(
        claims(realm_access={"roles": ["membership", "prodeko-org-superuser"]})
    )
    assert user.is_staff is True
    assert user.is_superuser is True


def test_losing_the_role_revokes_staff(backend):
    user = User.objects.create_user(
        email="maija@prodeko.org", keycloak_sub="sub-1", is_staff=True
    )
    updated = backend.update_user(user, claims())
    assert updated.is_staff is False


def test_adopting_a_stale_staff_row_does_not_escalate(backend):
    """A dormant admin account must not confer admin on whoever claims it."""
    User.objects.create_user(
        email="maija@prodeko.org", is_staff=True, is_superuser=True
    )
    user = backend.update_user(backend.filter_users_by_claims(claims())[0], claims())
    assert user.is_staff is False
    assert user.is_superuser is False


def test_inactive_row_is_reactivated_on_login(backend):
    """Keycloak would not have issued a token for a disabled account."""
    User.objects.create_user(
        email="maija@prodeko.org", keycloak_sub="sub-1", is_active=False
    )
    user = backend.update_user(User.objects.get(keycloak_sub="sub-1"), claims())
    assert user.is_active is True


# --- email changes -------------------------------------------------------


def test_email_change_in_keycloak_is_applied(backend):
    User.objects.create_user(email="old@prodeko.org", keycloak_sub="sub-1")
    user = backend.update_user(User.objects.get(keycloak_sub="sub-1"), claims())
    assert user.email == "maija@prodeko.org"


def test_email_change_colliding_with_another_row_is_refused(backend):
    User.objects.create_user(email="old@prodeko.org", keycloak_sub="sub-1")
    User.objects.create_user(email="maija@prodeko.org")
    with pytest.raises(SuspiciousOperation):
        backend.update_user(User.objects.get(keycloak_sub="sub-1"), claims())
