from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import EditProfileForm


@login_required
def profile(request):
    """Show and edit the parts of a profile that still live on this site."""

    if request.method == "POST":
        form = EditProfileForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if email and email != request.user.email:
                request.user.email = email
                request.user.save()
            return redirect(".")
    else:
        form = EditProfileForm(initial={"email": request.user.email})
    return render(request, "accounts/user_profile.html", {"form": form})


@login_required
def accept_policies(request):
    """Record that the member has accepted the privacy policy."""

    request.user.has_accepted_policies = True
    request.user.save()
    return redirect("/")
