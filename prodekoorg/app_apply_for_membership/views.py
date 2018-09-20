from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives

from .forms import PendingUserForm


def main_form(request):
    if request.method == 'POST':
        form_apply = PendingUserForm(request.POST, request.FILES)

        is_valid_form = form_apply.is_valid()

        if is_valid_form:
            form_apply.save()
            send_email()

            return render(request, 'hakemus_valmis.html')
        else:
            return render(request, 'apply_for_membership.html', {'form_apply': form_apply})
    elif request.is_ajax():
        pass
    else:
        form_apply = PendingUserForm()
        return render(request, 'apply_for_membership.html', {'form_apply': form_apply})


def send_email():
    # inform user about activation of credentials
    subject = 'Käyttäjätunnus aktivoitu'
    text_content = 'Käyttäjätunnuksesi {} on aktivoitu ja voit nyt kirjautua alumnirekisteriin.'.format(
        user.email)
    html_content = '<p>Käyttäjätunnuksesi <strong>{}</strong> on aktivoitu ja voit nyt kirjautua alumnirekisteriin.</p><br><p><a href="https://matrikkeli.prodeko.org">https://matrikkeli.prodeko.org</a></p>'.format(
        user.email)
    email_to = user.email
    from_email = 'alumnirekisteri.no.reply@prodeko.org'
    msg = EmailMultiAlternatives(
        subject, text_content, from_email, [email_to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()