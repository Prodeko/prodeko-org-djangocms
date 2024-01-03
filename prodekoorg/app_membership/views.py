from smtplib import SMTPAuthenticationError

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.template.loader import render_to_string

from .forms import PendingUserForm


def main_form(request):
    """Business logic behind the membership application form.

    Handles form submission by POST & AJAX, model creation from form data,
    form error handling as well as redirecting the user to a new page after
    a successful form submission.

    Args:
        request: HttpRequest object from Django.

    Returns:
        A Django TemplateResponse object that renders an html template.
    """

    if request.method == "POST" and request.is_ajax():
        form_apply = PendingUserForm(request.POST)
        is_valid_form = form_apply.is_valid()
        if is_valid_form:
            pending_user = form_apply.save(commit=False)

            if not pending_user.has_accepted_policies:
                return render(request, "app_membership_base.html", {"form": form_apply})
            pending_user.payment_intent_id = request.META.get("HTTP_X_PAYMENT_INTENT_ID")
            pending_user.save()
            try:
                send_email(pending_user)
            except SMTPAuthenticationError:
                # Google server doesn't authenticate no-reply@prodeko.org.
                # Most likely the password to said account is configured incorrectly
                return render(request, "app_membership_base.html", {"error": True})

            return render(request, "app_membership_base.html", {"done": True})
        else:
            # The http status code is captured as an error in javascript
            return render(request, "form_apply.html", {"form": form_apply}, status=599)
    else:
        form_apply = PendingUserForm()
        return render(request, "app_membership_base.html", {"form": form_apply})


def done(request):
    return render(request, "app_membership_base.html", {"done": True})

def send_email(user):
    """Send an information mail to mediakeisari@prodeko.org
    about a new PendingUser.

    Args:
        user: Django user

    Returns:
        Nothing, sends an email message.
    """

    subject = f"Uusi jäsenhakemus - {user.first_name} {user.last_name}"
    text_content = render_to_string("info_mail.txt", {"user": user})
    html_content = render_to_string("info_mail.html", {"user": user})

    # If DEBUG = True, email to DEV_EMAIL else email to mediakeisari@prodeko.org
    email_to = "mediakeisari@prodeko.org" if not settings.DEBUG else settings.DEV_EMAIL
    from_email = settings.DEFAULT_FROM_EMAIL
    msg = EmailMultiAlternatives(subject, text_content, from_email, [email_to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
