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
    return (claims.get(key) or "").strip()


def parse_claims(claims: dict) -> KeycloakIdentity:
    subject = _text(claims, "sub")
    if not subject:
        raise InvalidClaims("token has no sub claim")

    email = _text(claims, "email").lower()
    if not email:
        raise InvalidClaims("token has no email claim")

    roles = (claims.get("realm_access") or {}).get("roles") or []
    if isinstance(roles, str):
        # A User Realm Role mapper left non-multivalued emits a bare string.
        roles = [roles]

    return KeycloakIdentity(
        subject=subject,
        email=email,
        email_verified=bool(claims.get("email_verified")),
        first_name=_text(claims, "given_name"),
        last_name=_text(claims, "family_name"),
        roles=frozenset(roles),
    )
