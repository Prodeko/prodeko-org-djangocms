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


def test_break_glass_account_is_not_adopted_once_it_carries_a_subject(
    backend, settings
):
    """The exclusion has to cover the lookup by subject as well.

    Resolving by address is not the only way in: once a row carries a
    subject, every later login finds it that way instead. It is the one
    account left with a usable password, so adopting it by any route
    hands the last way into the site during a Keycloak outage to whoever
    registered the address.
    """
    settings.KEYCLOAK_BREAK_GLASS_EMAIL = "maija@prodeko.org"
    User.objects.create_user(
        email="maija@prodeko.org", keycloak_sub="sub-1", is_staff=True
    )
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


def test_a_login_cannot_demote_the_break_glass_account(backend, settings, monkeypatch):
    """Its staff flag is what lets it reach the admin, the only page that
    still takes a password. A login that stripped it would leave the
    account able to sign in and with nowhere to sign in to."""
    settings.KEYCLOAK_BREAK_GLASS_EMAIL = "maija@prodeko.org"
    User.objects.create_user(
        email="maija@prodeko.org",
        keycloak_sub="sub-1",
        is_staff=True,
        is_superuser=True,
    )

    with pytest.raises(SuspiciousOperation):
        resolve(backend, monkeypatch, claims())

    account = User.objects.get(email="maija@prodeko.org")
    assert account.is_staff is True
    assert account.is_superuser is True


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


def test_a_new_account_is_active(backend):
    user = backend.create_user(claims())
    assert user.is_active is True


# --- deactivated accounts -------------------------------------------------
#
# Deactivating an account is how the site takes someone out of the
# matrikkeli directory and its exports and off their own pages. Keycloak
# has no idea any of that happened and will keep issuing them tokens, so
# the refusal has to be made on this side, and it has to hold whichever
# way the identity would otherwise resolve.


def test_a_deactivated_account_is_refused_despite_the_role(backend):
    User.objects.create_user(
        email="maija@prodeko.org", keycloak_sub="sub-1", is_active=False
    )
    assert backend.verify_claims(claims()) is False


def test_a_deactivated_account_is_refused_by_address_too(backend):
    """It has never signed in through Keycloak, so the address is what
    would otherwise adopt it."""
    User.objects.create_user(email="maija@prodeko.org", is_active=False)
    assert backend.verify_claims(claims()) is False


def test_a_deactivated_account_is_not_adopted(backend):
    User.objects.create_user(email="maija@prodeko.org", is_active=False)
    with pytest.raises(SuspiciousOperation):
        backend.filter_users_by_claims(claims())


def test_a_deactivated_account_grandfathers_nobody(backend):
    """Otherwise registering a suspended member's address at Keycloak
    would pick up the flag that opens the site without a role."""
    User.objects.create_user(
        email="maija@prodeko.org", predates_keycloak=True, is_active=False
    )
    assert backend.verify_claims(claims(realm_access={"roles": []})) is False


def test_a_login_does_not_reactivate_a_deactivated_account(backend):
    """Nothing should reach update_user for such a row, but a login must
    not be able to undo an administrator's decision by any route: the
    person would silently reappear in the matrikkeli."""
    User.objects.create_user(
        email="maija@prodeko.org", keycloak_sub="sub-1", is_active=False
    )

    user = backend.update_user(User.objects.get(keycloak_sub="sub-1"), claims())

    assert user.is_active is False


def test_a_deactivated_address_is_not_handed_to_a_second_account(backend, monkeypatch):
    """email is unique, so a second row for the same address is a 500
    rather than a refusal, and adopting the first is what deactivation
    rules out. The whole login path has to end in neither."""
    User.objects.create_user(email="maija@prodeko.org", is_active=False)

    with pytest.raises(SuspiciousOperation):
        resolve(backend, monkeypatch, claims())

    assert User.objects.count() == 1


def test_reactivating_the_account_is_all_an_administrator_has_to_do(backend):
    """The refusal is theirs to lift, and lifting it should not also
    require unpicking a Keycloak link by hand."""
    account = User.objects.create_user(email="maija@prodeko.org", is_active=False)
    assert backend.verify_claims(claims()) is False

    User.objects.filter(pk=account.pk).update(is_active=True)

    assert backend.verify_claims(claims()) is True
    assert backend.filter_users_by_claims(claims())[0].pk == account.pk


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
