"""Resolving a Keycloak identity to a prodeko.org account.

Keycloak is the authority for who holds a membership and what they may
do: every login rewrites is_staff and is_superuser from the token, so a
privilege set locally cannot survive and a dormant admin row cannot be
inherited by whoever happens to claim its address.

Whether an account exists at all stays on this side. Only an active one
can be resolved to, so deactivating someone in the Django admin keeps
them off the site whatever Keycloak says about them.
"""

import logging

from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.utils import timezone
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from .claims import InvalidClaims, KeycloakIdentity, parse_claims

logger = logging.getLogger(__name__)


class KeycloakOIDCBackend(OIDCAuthenticationBackend):
    def get_userinfo(self, access_token, id_token, payload):
        """Merge the ID token's claims with the UserInfo response.

        The library resolves the account from this dict alone, and the
        realm-role mapper the setup guide specifies writes
        realm_access.roles to the ID token. Reading UserInfo only would
        make every login hinge on whether an administrator also ticked
        "Add to userinfo" on that mapper in the Keycloak admin console --
        a box nobody will think to look at once logins start failing.
        UserInfo is layered on top, so it wins where both define a claim:
        it is fetched now, whereas the ID token was minted at sign-in.
        """
        claims = dict(payload or {})
        claims.update(super().get_userinfo(access_token, id_token, payload))
        return claims

    def verify_claims(self, claims):
        try:
            identity = parse_claims(claims)
        except InvalidClaims as exc:
            logger.warning("Refusing Keycloak login: %s", exc)
            return False

        if not identity.email_verified:
            logger.warning(
                "Refusing Keycloak login for %s: email not verified", identity.email
            )
            return False

        occupant = self._occupant(identity)
        if occupant is not None and not occupant.is_active:
            logger.info(
                "Refusing Keycloak login for %s: the prodeko.org account is "
                "deactivated",
                identity.email,
            )
            return False

        if not self._may_sign_in(identity):
            logger.info(
                "Refusing Keycloak login for %s: no membership role and no "
                "account from before the migration",
                identity.email,
            )
            return False

        return True

    def _may_sign_in(self, identity: KeycloakIdentity) -> bool:
        """Whether Keycloak's word about this identity opens the site.

        A membership role does. So does an account that predates the
        migration, because nothing on prodeko.org consults membership
        status, so every former member holding one can sign in as things
        stand, and a role gate alone would take that away rather than
        keep it. The flag is false on every account created since, so a
        member who joins now and lapses later is refused; the membership
        registry closes that gap by issuing the alumni role, which is
        listed in the setting already.

        Deliberately asks for the rows the identity actually resolves to,
        so an address already claimed by another Keycloak subject, a
        deactivated account and the break-glass address vouch for nobody,
        and a stranger who self-registers matches nothing and is refused
        as before.
        """
        required = set(settings.KEYCLOAK_MEMBERSHIP_ROLES)
        if not required or identity.roles & required:
            return True

        return self._matching_accounts(identity).filter(predates_keycloak=True).exists()

    def _matching_accounts(self, identity: KeycloakIdentity):
        """The accounts this identity may be resolved to, if any.

        Adopts a legacy row by address, but never one already spoken for
        by a different Keycloak identity, never a deactivated one, and
        never the break-glass account, which has no Keycloak identity by
        design. Those last two rule out the subject lookup as well as the
        address lookup, so a link already recorded on such a row does not
        carry it past them.
        """
        adoptable = self.UserModel.objects.filter(is_active=True)
        if settings.KEYCLOAK_BREAK_GLASS_EMAIL:
            adoptable = adoptable.exclude(
                email__iexact=settings.KEYCLOAK_BREAK_GLASS_EMAIL
            )

        by_subject = adoptable.filter(keycloak_sub=identity.subject)
        if by_subject.exists():
            return by_subject

        return adoptable.filter(email__iexact=identity.email, keycloak_sub__isnull=True)

    def _occupant(self, identity: KeycloakIdentity):
        """The account standing in this identity's way, if any.

        Looked up the way _matching_accounts resolves -- subject first,
        then address -- so this is the row that lookup turned down, and
        the one an administrator has to act on.
        """
        return (
            self.UserModel.objects.filter(keycloak_sub=identity.subject).first()
            or self.UserModel.objects.filter(email__iexact=identity.email).first()
        )

    def _refusal(self, occupant) -> str:
        """Why that account cannot be resolved to, in an admin's terms."""
        if settings.KEYCLOAK_BREAK_GLASS_EMAIL and (
            occupant.email.lower() == settings.KEYCLOAK_BREAK_GLASS_EMAIL.lower()
        ):
            return (
                "it is the break-glass account, which has no Keycloak "
                "identity by design"
            )
        if not occupant.is_active:
            return "the prodeko.org account it resolves to is deactivated"
        return f"it is already linked to Keycloak subject {occupant.keycloak_sub}"

    def filter_users_by_claims(self, claims):
        identity = parse_claims(claims)

        candidates = self._matching_accounts(identity)
        if candidates.exists():
            return candidates

        # Nothing survived the filter. The library reads that as "no such
        # user, create one", and email is unique, so an address that is
        # taken by a row we refuse to adopt has to be refused out loud
        # instead. SuspiciousOperation is what the library's authenticate()
        # catches, which lands the browser on the login-failure page.
        occupant = self._occupant(identity)
        if occupant is None:
            return candidates

        reason = self._refusal(occupant)
        logger.warning(
            "Refusing Keycloak login for %s (subject %s): %s",
            identity.email,
            identity.subject,
            reason,
        )
        raise SuspiciousOperation(
            f"Keycloak identity {identity.email} (subject {identity.subject}) "
            f"cannot be signed in because {reason}; an administrator must "
            f"resolve this by hand"
        )

    def create_user(self, claims):
        # The library's create_user calls create_user(username, email=...),
        # which our email-as-username manager does not accept.
        identity = parse_claims(claims)
        user = self.UserModel.objects.create_user(
            email=identity.email,
            first_name=identity.first_name,
            last_name=identity.last_name,
        )
        logger.info("Created prodeko.org account for %s", identity.email)
        return self._apply(user, identity)

    def update_user(self, user, claims):
        return self._apply(user, parse_claims(claims))

    def _apply(self, user, identity: KeycloakIdentity):
        if user.keycloak_sub and user.keycloak_sub != identity.subject:
            raise SuspiciousOperation(
                f"Account {user.pk} is linked to a different Keycloak subject"
            )

        if not user.keycloak_sub:
            user.keycloak_sub = identity.subject
            user.keycloak_linked_at = timezone.now()
            logger.info(
                "Linked %s to Keycloak subject %s", user.email, identity.subject
            )

        if user.email.lower() != identity.email:
            taken = (
                self.UserModel.objects.filter(email__iexact=identity.email)
                .exclude(pk=user.pk)
                .exists()
            )
            if taken:
                # Merging the two rows is a judgement call about someone's
                # data, so it belongs to an administrator, not to a login.
                raise SuspiciousOperation(
                    f"Keycloak address {identity.email} already belongs to "
                    f"another prodeko.org account; merge them by hand"
                )
            user.email = identity.email

        user.first_name = identity.first_name
        user.last_name = identity.last_name
        # is_active is left alone. Keycloak enabling an account says
        # nothing about whether prodeko.org wants it: deactivating someone
        # here is what takes them out of the matrikkeli, and a login must
        # not undo it. Such a row is refused before this point anyway.
        user.is_superuser = settings.KEYCLOAK_SUPERUSER_ROLE in identity.roles
        user.is_staff = (
            user.is_superuser or settings.KEYCLOAK_STAFF_ROLE in identity.roles
        )
        user.save()
        return user
