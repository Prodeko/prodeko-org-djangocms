from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render

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
    # inform user about activation of credentials
    subject = 'Uusi jäsenhakemus - {}'.format(user.name)
    text_content = '{} hakee Prodekon jäsenyyttä' \
        '- {} \n - {}, {} \n - {} \n - {} \n - {} \n\n https://prodeko.org//fi/admin/app_apply_for_membership/pendinguser/' + str(user.id) + '/change/ - Hyväksy tai hylkää hakemus'.format(
            user.name, user.email, user.field_of_study, user.start_year, user.hometown, user.membership_type, user.additional_info)
    html_content = '<p><strong>{}</strong> hakee Prodekon jäsenyyttä.' \
        '<ul><li>{}</li><li>{}, {}</li><li>{}</li><li>{}</li><li>{}</li></ul>'
    '</p><br><p><a href="https://prodeko.org//fi/admin/app_apply_for_membership/pendinguser/' + str(user.id) + '/change/">Hyväksy tai hylkää hakemus</a></p>'.format(
        user.name, user.email, user.field_of_study, user.start_year, user.hometown, user.membership_type, user.additional_info)
    email_to = 'mediakeisari@prodeko.org'
    from_email = settings.DEFAULT_FROM_EMAIL
    msg = EmailMultiAlternatives(subject, text_content, from_email, [email_to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
