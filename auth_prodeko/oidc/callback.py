"""Telling an expired sign-in apart from a refused one."""

import logging
import time
from urllib.parse import urlencode

import requests
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse
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
    then refuses: a revoked role, an address already linked to another
    Keycloak subject, an attempt to adopt the break-glass account. That
    is what the failure page is for. The base view only redirects there,
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
        except requests.exceptions.RequestException:
            # Every way a call to Keycloak can fail arrives here: a
            # timeout cut off by OIDC_TIMEOUT, a refused connection, a
            # 503 from the token endpoint. Nothing between here and
            # requests catches any of them, so without this the member
            # gets a 500 and the admins get mail for every click for as
            # long as the outage lasts. Warning, not error: the site is
            # fine, Keycloak is not, and ERROR is what the production
            # LOGGING config mails on.
            logger.warning("Keycloak did not answer; refusing the login", exc_info=True)
            return self.login_failure()

    def login_failure(self):
        if self.request.GET.get("error") in SILENT_REFRESH_ERRORS:
            return self.session_expired()
        session = self.request.session
        expired = session.get("oidc_id_token_expiration", 0) <= time.time()
        if expired and self.request.user.is_authenticated:
            auth.logout(self.request)
        return super().login_failure()

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
