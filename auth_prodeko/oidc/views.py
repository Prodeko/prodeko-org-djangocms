"""Views that keep the old login URL names pointing somewhere useful.

Seventy decorators, LOGIN_URL, the navbar and the policy modal all name
auth_prodeko:login. Keeping the name and swapping the view behind it is
what stops this migration from touching all of them.
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
