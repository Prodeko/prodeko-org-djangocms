"""The view auth_prodeko:login points at.

LOGIN_URL names auth_prodeko:login, the navbar links to it, and so does
every login_required decorator in the project by way of LOGIN_URL. One
view behind that name is what spares all of them from knowing where
sign-in actually happens.
"""

from django.urls import reverse
from django.utils.http import urlencode
from django.views.generic import RedirectView


class OIDCLoginRedirectView(RedirectView):
    permanent = False
    query_string = False

    def get_redirect_url(self, *args, **kwargs):
        url = reverse("oidc_authentication_init")
        next_url = self.request.GET.get("next")
        if next_url:
            url = f"{url}?{urlencode({'next': next_url})}"
        return url
