from smtplib import SMTPAuthenticationError

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.template.loader import render_to_string

from .forms import ContactForm


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

        form_contact = ContactForm(request.POST, request.FILES)
        is_valid_form = form_contact.is_valid()
        if is_valid_form:
            message = form_contact.save(commit=False)

            if message.email and not message.has_accepted_policies:
                return render(request, "app_contact_base.html", {"form": form_contact})

            message.save()
            try:
                send_email(message)
            except SMTPAuthenticationError:
                # Google server doesn't authenticate no-reply@prodeko.org.
                # Most likely the password to said account is configured incorrectly
                return render(request, "app_contact_base.html", {"error": True})

            return render(request, "app_contact_base.html", {"done": True})
        else:
            # The http status code is captured as an error in javascript
            return render(
                request, "form_contact.html", {"form": form_contact}, status=599
            )
    else:
        form_contact = ContactForm()
        return render(request, "app_contact_base.html", {"form": form_contact})


def send_email(message):
    """Send contact form message to hallitus@prodeko.org

    Args:
        message: Message object

    Returns:
        Nothing, sends an email message.
    """

    subject = "Viesti prodeko.org yhteydenottolomakkeesta"
    text_content = render_to_string("message_mail.txt", {"message": message})
    html_content = render_to_string("message_mail.html", {"message": message})

    # If DEBUG = True, email to DEV_EMAIl else email to selected contact email
    email_to = (
        message.get_contact_emails_display()
        if not settings.DEBUG
        else settings.DEV_EMAIL
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    msg = EmailMultiAlternatives(subject, text_content, from_email, [email_to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
