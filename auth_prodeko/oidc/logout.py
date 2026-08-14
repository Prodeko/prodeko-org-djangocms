"""Ending the Keycloak session as well as the Django one."""

from django.conf import settings
from django.utils.http import urlencode


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
