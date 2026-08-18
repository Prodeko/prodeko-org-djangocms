"""Logging out: the URL Keycloak is sent to, and the view that sends it."""

from django.conf import settings
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.utils.http import urlencode
from mozilla_django_oidc.views import OIDCLogoutView


def provider_logout(request) -> str:
    # Keycloak refuses a post_logout_redirect_uri that is backed by
    # neither a client id nor an id token hint, and the break-glass
    # account signs in without ever holding an id token.
    params = {
        "post_logout_redirect_uri": request.build_absolute_uri(
            settings.LOGOUT_REDIRECT_URL
        ),
        "client_id": settings.OIDC_RP_CLIENT_ID,
    }
    id_token = request.session.get("oidc_id_token")
    if id_token:
        params["id_token_hint"] = id_token
    return f"{settings.OIDC_OP_LOGOUT_ENDPOINT}?{urlencode(params)}"


class AdminLogoutView(OIDCLogoutView):
    """Logout that the django-cms toolbar can call without an error.

    The toolbar renders its Logout button as an AJAX POST to the admin
    logout URL. A full RP-initiated logout answers 302 to Keycloak; the
    XHR follows that cross-origin, the response carries no CORS headers,
    the call fails, and the editor gets an error banner over a logout
    that in fact worked. So an XHR is answered with the local session
    flushed and a same-origin redirect it can follow.

    The trade-off, taken deliberately: an editor who logs out from the
    toolbar ends their prodeko.org session but not their Keycloak one,
    so a click on a login link signs them straight back in without a
    password prompt. Ending the Keycloak session too needs a full-page
    navigation, which is what every other way of logging out — the
    site's logout link, the admin, typing the URL — is.
    """

    def post(self, request):
        if request.headers.get("x-requested-with") != "XMLHttpRequest":
            return super().post(request)
        auth.logout(request)
        return HttpResponseRedirect(self.redirect_url)
