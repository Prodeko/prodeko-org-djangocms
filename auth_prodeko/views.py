from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .oidc import refusal
from .oidc.logout import provider_logout


@login_required
def profile(request):
    """Show the parts of a profile that this site knows about."""

    return render(request, "accounts/user_profile.html")


def login_failed(request):
    """Explain a sign-in that Keycloak allowed and this site did not.

    The refusal leaves its reason in the session, named by the errand it
    puts the visitor on: renew a membership, write to an administrator
    about an account conflict, or simply try again once Keycloak
    answers. The page says which errand and no more -- never which check
    fired, so a conflict does not spell out whose address is linked
    where. With no reason recorded it falls back to the membership
    explanation, the reason the page is mostly here for.

    The Keycloak session outlives the refusal, so the login link would
    sign the visitor straight back into the same bounce. The sign-out
    link is built here rather than pointing at auth_prodeko:logout,
    which only reaches Keycloak for a visitor who has a Django session;
    a refused visitor has none.
    """

    return render(
        request,
        "accounts/login_failed.html",
        {
            "keycloak_logout_url": provider_logout(request),
            "refusal": refusal.pop(request),
        },
    )


@login_required
def accept_policies(request):
    """Record that the member has accepted the privacy policy."""

    request.user.has_accepted_policies = True
    request.user.save()
    return redirect("/")
