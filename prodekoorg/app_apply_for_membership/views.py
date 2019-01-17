import configparser
import os

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.template.loader import render_to_string

from .forms import PendingUserForm


def main_form(request):
    if request.method == 'POST' and request.is_ajax():

        form_apply = PendingUserForm(request.POST, request.FILES)
        is_valid_form = form_apply.is_valid()
        if is_valid_form:
            pending_user = form_apply.save()
            send_email(pending_user)

            return render(request, 'app_base.html', {'done': True})
        else:
            # The http status code is captured as an error in javascript
            return render(request, 'form_apply.html', {'form': form_apply}, status=599)
    else:
        form_apply = PendingUserForm()
        return render(request, 'app_base.html', {'form': form_apply})


def send_email(user):
    # Inform mediakeisari about new user
    subject = 'Uusi jäsenhakemus - {}'.format(user.name)
    text_content = render_to_string('info_mail.txt', {'user': user})
    html_content = render_to_string('info_mail.html', {'user': user})

    # If DEBUG = True, email to DEV_EMAIl else
    # email to mediakeisari@prodeko.org
    config = configparser.ConfigParser()
    config.read(os.path.join(settings.BASE_DIR, 'prodekoorg/variables.txt'))

    email_to = 'mediakeisari@prodeko.org' if not settings.DEBUG else config['EMAIL']['DEV_EMAIL'] 
    from_email = settings.DEFAULT_FROM_EMAIL
    msg = EmailMultiAlternatives(subject, text_content, from_email, [email_to])
    msg.attach_alternative(html_content, "text/html")
    msg.attach('receipt.jpg', user.receipt.file.read(), 'image/jpg')
    msg.send()
