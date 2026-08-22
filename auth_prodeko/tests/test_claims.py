import pytest

from auth_prodeko.oidc.claims import InvalidClaims, parse_claims


def claims(**overrides):
    base = {
        "sub": "9f1c-uuid",
        "email": "Maija.Meikalainen@prodeko.org",
        "email_verified": True,
        "given_name": "Maija",
        "family_name": "Meikäläinen",
        "realm_access": {"roles": ["membership", "prodeko-org-admin"]},
    }
    base.update(overrides)
    return base


def test_parses_a_complete_token():
    identity = parse_claims(claims())
    assert identity.subject == "9f1c-uuid"
    assert identity.first_name == "Maija"
    assert identity.last_name == "Meikäläinen"
    assert identity.email_verified is True
    assert identity.roles == frozenset({"membership", "prodeko-org-admin"})


def test_email_is_lowercased_and_stripped():
    identity = parse_claims(claims(email="  Maija@Prodeko.ORG "))
    assert identity.email == "maija@prodeko.org"


def test_missing_subject_is_rejected():
    with pytest.raises(InvalidClaims):
        parse_claims(claims(sub=""))


def test_missing_email_is_rejected():
    payload = claims()
    del payload["email"]
    with pytest.raises(InvalidClaims):
        parse_claims(payload)


def test_absent_email_verified_is_false_not_none():
    identity = parse_claims(claims(email_verified=None))
    assert identity.email_verified is False


def test_string_email_verified_is_not_trusted():
    """The sole guard on adopting a legacy row by address is not truthiness."""
    assert parse_claims(claims(email_verified="false")).email_verified is False
    assert parse_claims(claims(email_verified="true")).email_verified is False
    assert parse_claims(claims(email_verified=1)).email_verified is False


def test_absent_realm_access_yields_no_roles():
    payload = claims()
    del payload["realm_access"]
    assert parse_claims(payload).roles == frozenset()


def test_single_valued_roles_claim_is_tolerated():
    """A mapper configured non-multivalued emits a bare string."""
    identity = parse_claims(claims(realm_access={"roles": "membership"}))
    assert identity.roles == frozenset({"membership"})


def test_missing_names_become_empty_strings():
    payload = claims()
    del payload["given_name"]
    del payload["family_name"]
    identity = parse_claims(payload)
    assert identity.first_name == ""
    assert identity.last_name == ""


# --- malformed payloads ---------------------------------------------------
#
# A misconfigured mapper can emit any JSON type. The parser must refuse
# such a token, never raise something the caller does not catch.


def test_non_string_names_become_empty_strings():
    identity = parse_claims(claims(given_name=42, family_name=["Meikalainen"]))
    assert identity.first_name == ""
    assert identity.last_name == ""


def test_non_string_subject_is_rejected():
    with pytest.raises(InvalidClaims):
        parse_claims(claims(sub=12345))


def test_non_string_email_is_rejected():
    with pytest.raises(InvalidClaims):
        parse_claims(claims(email={"value": "maija@prodeko.org"}))


def test_non_dict_realm_access_yields_no_roles():
    assert parse_claims(claims(realm_access="membership")).roles == frozenset()


def test_non_string_roles_are_dropped():
    identity = parse_claims(
        claims(realm_access={"roles": ["membership", {"name": "admin"}, None]})
    )
    assert identity.roles == frozenset({"membership"})
