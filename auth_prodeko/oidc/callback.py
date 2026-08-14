"""Turning a refused re-authentication into a sign-out."""

import time

from django.contrib import auth
from mozilla_django_oidc.views import OIDCAuthenticationCallbackView


class KeycloakOIDCCallbackView(OIDCAuthenticationCallbackView):
    """Ends the Django session when Keycloak's answer is refused.

    SessionRefresh sends a session whose id token has aged out back to
    Keycloak with prompt=none. Keycloak answers a member whose role was
    revoked with a perfectly valid code, and the backend then refuses
    the claims behind it. The base view only redirects to the failure
    url, so the session stays authenticated with an id token still
    recorded as expired, and the very next request is sent round again:
    a redirect loop with no page to log out from. Signing the user out
    is what makes the revocation land.

    The sign-out is limited to sessions the recheck would bounce, so a
    stray GET of the callback url cannot log a working session out.
    """

    def login_failure(self):
        session = self.request.session
        expired = session.get("oidc_id_token_expiration", 0) <= time.time()
        if expired and self.request.user.is_authenticated:
            auth.logout(self.request)
        return super().login_failure()
