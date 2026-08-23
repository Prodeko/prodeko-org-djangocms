"""Carrying the reason for a refused sign-in to the failure page.

authenticate() answers the callback view with None whichever check
refused, and the failure page is a redirect away from both, so the
reason travels through the session. The codes name what the visitor can
act on, not which check fired: a deactivated account and a taken
address are different checks but the same errand to an administrator.
"""

NO_MEMBERSHIP = "no_membership"
ACCOUNT_CONFLICT = "account_conflict"
PROVIDER_UNAVAILABLE = "provider_unavailable"

SESSION_KEY = "keycloak_refusal"

_KNOWN = frozenset({NO_MEMBERSHIP, ACCOUNT_CONFLICT, PROVIDER_UNAVAILABLE})


def stash(request, reason):
    """Record the reason, on the paths that have a request to record on.

    The backend also runs outside authenticate() -- tests, shell -- with
    no request attached, and a refusal there has nowhere to leave its
    reason. That must not turn it into a crash.
    """
    if request is None:
        return
    request.session[SESSION_KEY] = reason


def pop(request):
    """The reason for the refusal that led here, spent on reading.

    Spent, so a reason cannot outlive its refusal and explain some
    later, unrelated failure. A value outside the known codes reads as
    no reason at all.
    """
    reason = request.session.pop(SESSION_KEY, None)
    return reason if reason in _KNOWN else None
