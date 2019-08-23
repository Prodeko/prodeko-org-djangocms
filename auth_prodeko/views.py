from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import EditProfileForm


@login_required(login_url="/login/")
def profile(request):
    """Business logic behind the EditProfileForm.

    Args:
        request: HttpRequest object from Django.

    Returns:
        A Django TemplateResponse object that renders an html template,
        or refreshes the page on successful form submission.
    """

    # Handle updating user profile
    if request.method == "POST":
        form = EditProfileForm(request.user, data=request.POST)
        if form.is_valid():
            user = request.user
            email = form.data["email"]
            password = form.data["password"]
            newpassword = form.data["newpassword"]
            if email != user.email:
                user.email = email
            if newpassword:
                if newpassword != password:
                    user.set_password(newpassword)
                    # Prevent user from being logged out of the session
                    update_session_auth_hash(request, user)
            user.save()
            return redirect(".")
    # Else display user profile page with edit form
    else:
        form = EditProfileForm(request.user, initial={"email": request.user.email})
    return render(request, "accounts/user_profile.html", {"form": form})


def accept_policies(request):
    """Update user with has_accepted_policies = True

    Args:
        request: HttpRequest object from Django.

    Returns:
        Refreshes the page.
    """

    user = request.user
    user.has_accepted_policies = True
    user.save()
    return redirect(".")
