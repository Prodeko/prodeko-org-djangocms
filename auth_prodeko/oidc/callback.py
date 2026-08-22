"""Telling an expired sign-in apart from a refused one."""

import logging
import time
from urllib.parse import urlencode

import requests
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.module_loading import import_string
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from mozilla_django_oidc.views import OIDCAuthenticationCallbackView

logger = logging.getLogger(__name__)

# The errors only a prompt=none handoff can come back with. Every one of
# them means the same thing: Keycloak could not answer without the member
# in front of it, because the SSO session had ended or it wanted them to
# act. None of them says anything about their right to be here.
SILENT_REFRESH_ERRORS = frozenset(
    {
        "login_required",
        "interaction_required",
        "consent_required",
        "account_selection_required",
    }
)


class KeycloakOIDCCallbackView(OIDCAuthenticationCallbackView):
    """Splits an expired Keycloak session off from a refused identity.

    SessionRefresh sends a session whose id token has aged out back to
    Keycloak with prompt=none, and the answer comes back one of two
    ways.

    Keycloak's SSO session ends long before Django's thirty days, so for
    every member, roughly daily, the answer is error=login_required.
    That is an ordinary expiry: the member signs in again and carries
    on, and the failure page, which talks about membership, would be a
    false accusation.

    The other way is a perfectly valid code whose claims the backend
    then refuses: a revoked role, a deactivated account, an address
    already linked to another Keycloak subject, an attempt to adopt the
    break-glass account. That is what the failure page is for, and the
    member has to see it. The base view only redirects there,
    leaving the session authenticated with an id token still recorded as
    expired, so the very next request is sent round again: a redirect
    loop with no page to log out from. Signing the user out is what
    makes the refusal land.

    The sign-out is limited to sessions the recheck would bounce, so a
    stray GET of the callback url cannot log a working session out.
    """

    interrupted_page = None

    def get(self, request):
        # The base view ends the Django session before login_failure()
        # runs, and the page the member was reading goes with it.
        self.interrupted_page = request.session.get("oidc_login_next")
        try:
            return super().get(request)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            # Keycloak never answered: a refused connection, a name that
            # does not resolve, a request cut off by OIDC_TIMEOUT.
            # Nothing between here and requests catches any of them, so
            # without this the member gets a 500 and the admins get mail
            # for every click for as long as the outage lasts. Warning,
            # not error: the site is fine, Keycloak is not, and ERROR is
            # what the production LOGGING config mails on.
            logger.warning("Keycloak did not answer; refusing the login", exc_info=True)
            return self.login_failure()
        except requests.exceptions.RequestException:
            # Keycloak answered and the answer was unusable: a 401 from
            # the token endpoint because the client secret here does not
            # match the one in the realm, a body that is not JSON. That
            # is a fault in this deployment, it will not clear on its
            # own, and every login fails until someone fixes it, so it is
            # worth the mail ERROR sends.
            logger.error(
                "Keycloak rejected this site's own credentials or answered "
                "unintelligibly; refusing the login",
                exc_info=True,
            )
            return self.login_failure()

    def login_failure(self):
        if self.request.GET.get("error") in SILENT_REFRESH_ERRORS:
            return self.session_expired()
        if self._recheck_would_bounce():
            auth.logout(self.request)
        return super().login_failure()

    def _recheck_would_bounce(self) -> bool:
        """Whether SessionRefresh would send this session round again.

        Its two conditions in its own terms: the session was
        authenticated by an OIDC backend, and its id token has aged out.
        The backend is the load-bearing one. A session with no id token
        at all reads as one whose token expired long ago, and that is
        the break-glass account, sitting in the admin through
        ModelBackend precisely because Keycloak cannot be reached -- so
        without this test a stray GET of the callback url would end the
        one session that still works.
        """
        session = self.request.session
        if not self.request.user.is_authenticated:
            return False
        backend = session.get(auth.BACKEND_SESSION_KEY)
        if backend and not issubclass(
            import_string(backend), OIDCAuthenticationBackend
        ):
            return False
        return session.get("oidc_id_token_expiration", 0) <= time.time()

    def session_expired(self):
        """Sends the member into the ordinary interactive login.

        The base view has already ended the Django session, so this
        redirect passes SessionRefresh untouched and the login view
        hands the browser straight to Keycloak's own form: one hop out
        of the site rather than a ring of two urls inside it.
        """
        url = reverse("oidc_authentication_init")
        if self.interrupted_page:
            url = f"{url}?{urlencode({'next': self.interrupted_page})}"
        return HttpResponseRedirect(url)
