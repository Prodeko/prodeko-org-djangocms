"""Turning a Keycloak token payload into the facts prodeko.org needs.

Deliberately pure: no database, no request, no network. Everything that
can go wrong in the mapping is therefore testable from a dict literal.
"""

from dataclasses import dataclass


class InvalidClaims(ValueError):
    """The token payload lacks something we cannot proceed without."""


@dataclass(frozen=True)
class KeycloakIdentity:
    subject: str
    email: str
    email_verified: bool
    first_name: str
    last_name: str
    roles: frozenset[str]


def _text(claims: dict, key: str) -> str:
    # A misconfigured mapper can put any JSON type here. Anything that is
    # not a string is absent as far as we are concerned, so that a
    # malformed token is refused rather than raising out of the callback.
    value = claims.get(key)
    return value.strip() if isinstance(value, str) else ""


def _roles(realm_access) -> frozenset[str]:
    if not isinstance(realm_access, dict):
        return frozenset()

    roles = realm_access.get("roles")
    if isinstance(roles, str):
        # A User Realm Role mapper left non-multivalued emits a bare string.
        return frozenset({roles})
    if isinstance(roles, (list, tuple, set, frozenset)):
        return frozenset(role for role in roles if isinstance(role, str))
    return frozenset()


def parse_claims(claims: dict) -> KeycloakIdentity:
    subject = _text(claims, "sub")
    if not subject:
        raise InvalidClaims("token has no sub claim")

    email = _text(claims, "email").lower()
    if not email:
        raise InvalidClaims("token has no email claim")

    return KeycloakIdentity(
        subject=subject,
        email=email,
        # This is the sole guard on adopting a legacy row by address, so
        # only the boolean true counts; a truthy "false" must not pass.
        email_verified=claims.get("email_verified") is True,
        first_name=_text(claims, "given_name"),
        last_name=_text(claims, "family_name"),
        roles=_roles(claims.get("realm_access")),
    )
