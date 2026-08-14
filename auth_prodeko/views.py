from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def profile(request):
    """Show the parts of a profile that this site knows about."""

    return render(request, "accounts/user_profile.html")


@login_required
def accept_policies(request):
    """Record that the member has accepted the privacy policy."""

    request.user.has_accepted_policies = True
    request.user.save()
    return redirect("/")
