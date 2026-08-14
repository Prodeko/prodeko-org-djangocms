from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .oidc.logout import provider_logout


@login_required
def profile(request):
    """Show the parts of a profile that this site knows about."""

    return render(request, "accounts/user_profile.html")


def login_failed(request):
    """Explain a sign-in Keycloak allowed but this site refused.

    Three refusals lead here: no membership role, an address already
    linked to another Keycloak identity, and an attempt to adopt the
    break-glass account. The visitor is told what they can act on -- the
    site is for members -- and never which of the three it was.

    The Keycloak session outlives the refusal, so the login link would
    sign the visitor straight back into the same bounce. The sign-out
    link is built here rather than pointing at auth_prodeko:logout,
    which only reaches Keycloak for a visitor who has a Django session;
    a refused visitor has none.
    """

    return render(
        request,
        "accounts/login_failed.html",
        {"keycloak_logout_url": provider_logout(request)},
    )


@login_required
def accept_policies(request):
    """Record that the member has accepted the privacy policy."""

    request.user.has_accepted_policies = True
    request.user.save()
    return redirect("/")
