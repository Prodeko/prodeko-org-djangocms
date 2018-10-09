import json

from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render

from .forms import PendingUserForm


 # TODO: Display error message if email already exists in the database
def main_form(request):
    if request.method == 'POST' and request.is_ajax():

        json_form_data = json.loads(request.body.decode('utf-8'))
        form_data = {}
        for i, entry in enumerate(json_form_data):
            form_data[entry['name']] = entry['value']

        form_apply = PendingUserForm(form_data, request.FILES)
        is_valid_form = form_apply.is_valid()

        if is_valid_form:
            pending_user = form_apply.save()
            print(pending_user)
            # send_email(pending_user)

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
        '- {} \n - {}, {} \n - {} \n - {} \n - {} \n\n https://prodeko.org//fi/admin/app_apply_for_membership/pendinguser/' + user.id + '/change/ - Hyväksy tai hylkää hakemus'.format(
            user.name, user.email, user.field_of_study, user.start_year, user.hometown, user.membership_type, user.additional_info)
    html_content = '<p><strong>{}</strong> hakee Prodekon jäsenyyttä.' \
        '<ul><li>{}</li><li>{}, {}</li><li>{}</li><li>{}</li><li>{}</li></ul>'
    '</p><br><p><a href="https://prodeko.org//fi/admin/app_apply_for_membership/pendinguser/' + user.id + '/change/">Hyväksy tai hylkää hakemus</a></p>'.format(
        user.name, user.email, user.field_of_study, user.start_year, user.hometown, user.membership_type, user.additional_info)
    email_to = 'mediakeisari@prodeko.org'
    from_email = 'no-reply@prodeko.org'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [email_to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()