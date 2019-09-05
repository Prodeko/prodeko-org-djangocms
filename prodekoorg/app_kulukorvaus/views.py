from smtplib import SMTPAuthenticationError

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.core.mail import EmailMultiAlternatives
from django.forms import formset_factory
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from .forms import KulukorvausForm, KulukorvausPerustiedotForm
from .models import KulukorvausPerustiedot
from .printing import KulukorvausPDF


@login_required
def download_kulukorvaus_pdf(request, perustiedot_id):
    """Downloads a Kulukorvaus model as PDF

    Retrieves the pdf associated with a KulukorvausPerustiedot model
    and return a HttpResponse with the pdf attached.

    Args:
        request: HttpRequest object from Django.
        perustiedot_id: id of the KulukorvausPerustiedot model whose
            pdf is being requested.

    Returns:
        HttpResponse with the pdf file attached.

        If the user isn't logged in, they are redirected to the login url.

    Raises:
        Http404: Kulukorvaus (reimbursement) model does not exist.
        PermissionDenied: User didn't create the reimbursement.
    """

    # Try to fetch the KulukorvausPerustiedot object. If it doesn't
    # exist, raise HTTP404. If the user doesn't own the object or if they do not have admin permissions
    # raise PermissionDenied.
    try:
        model_perustiedot = KulukorvausPerustiedot.objects.get(id=perustiedot_id)
        if (
            not request.user == model_perustiedot.created_by_user
            and not request.user.is_staff
        ):
            raise PermissionDenied
    except KulukorvausPerustiedot.DoesNotExist:
        raise Http404("Reimbursement does not exist")

    # Create the HttpResponse object with the appropriate PDF headers.
    filename = model_perustiedot.pdf_filename()
    response = HttpResponse(model_perustiedot.pdf.file, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="' + filename + '"'
    return response


def add_pdf_to_model(perustiedot_id):
    """Helper function to add a pdf file to the KulukorvausPerustiedot model.

    Retrieves all of the Kulukorvaus models associated with a
    KulukorvausPerustiedot model, initializes a KulukorvausPDF class
    that abstracts away the pdf generation, generates the pdf via
    a call to print_kulukorvaukset() and appends the generated pdf
    to the KulukorvausPerustiedot model.

    Args:
        perustiedot_id: id of the KulukorvausPerustiedot object
            to which we want to add a pdf file.

    Returns:
        Nothing, adds a pdf to a KulukorvausPerustiedot model.
    """

    model_perustiedot = KulukorvausPerustiedot.objects.get(id=perustiedot_id)
    # This fetches all the Kulukorvaus objects whose 'info' foreign key
    # attribute is the KulukorvausPerustiedot object obtained above.
    models_kulukorvaukset = model_perustiedot.kulukorvaus_set.all()

    # Initialize class KulukorvausPDF defined in printing.py and
    # generate the pdf based on KulukorvausPerustiedot and
    # Kulukorvaus object data.
    kulukorvaus = KulukorvausPDF(model_perustiedot, models_kulukorvaukset)
    pdf = kulukorvaus.print_kulukorvaukset()

    # Set the 'pdf' attribute of model KulukorvausPerustiedot.
    pdf_file = ContentFile(pdf)
    filename = model_perustiedot.pdf_filename()
    model_perustiedot.pdf.save(filename, pdf_file)


@login_required
def main_form(request):
    """Processing logic behind the form at url /kulukorvaus.

    Handles form submission by POST & AJAX, model creation from form data,
    form error handling as well as redirecting the user to a new page after
    a successful form submission.

    Args:
        request: HttpRequest object from Django.

    Returns:
        A Django TemplateResponse object that renders an html template.

        If the user isn't logged in, they are redirected to the login url.
    """

    # If the user hasn't accepted Prodeko's privacy policy
    # return a 'policy error' page.
    if not request.user.has_accepted_policies:
        return render(request, "kulukorvaus.html", {"policy_error": True})

    # Django docs: "A formset is a layer of abstraction to work
    # with multiple forms on the same page." In this case we might
    # have multiple KulukorvausForms in the same page but only one
    # KulukorvausPerustiedotForm.
    KulukorvausFormset = formset_factory(KulukorvausForm)
    if request.method == "POST" and request.is_ajax():

        # Generate form objects from POST data.
        form_perustiedot = KulukorvausPerustiedotForm(request.POST)
        formset = KulukorvausFormset(request.POST, request.FILES)

        # Check that the forms are valid.
        is_valid_perustiedot = form_perustiedot.is_valid()
        is_valid_formset = formset.is_valid()

        if is_valid_perustiedot and is_valid_formset:
            # Forms are valid, create objects from form data.
            model_perustiedot = form_perustiedot.save(commit=False)
            model_perustiedot.created_by_user = request.user
            model_perustiedot.save()

            # Loop KulukorvausForms in the formset, associate
            # them with a KulukorvausPerustiedot and save.
            for form in formset:
                model = form.save(commit=False)
                model.info = model_perustiedot
                model.save()

            try:
                # Helper function to generate a pdf representing
                # the whole reimbursemet. Adds the generated pdf
                # to the KulukorvausPerustiedot object created above.
                add_pdf_to_model(model_perustiedot.id)
            except:
                # Something went wrong in PDF generation
                return render(request, "kulukorvaus.html", {"error": True})

            try:
                # Send email to the person who submitted the kulukorvaus
                send_email(
                    request.user,
                    model_perustiedot.id,
                    "kulukorvaus.txt",
                    model_perustiedot.email,
                )

                # Send email to rahastonhoitaja@prodeko.org, or DEV_EMAIL if we are in debug mode.
                email_to = (
                    "rahastonhoitaja@prodeko.org"
                    if not settings.DEBUG
                    else settings.DEV_EMAIL
                )
                send_email(
                    request.user,
                    model_perustiedot.id,
                    "kulukorvaus_rahastonhoitaja.txt",
                    email_to,
                )
            except SMTPAuthenticationError:
                # Google server doesn't authenticate no-reply@prodeko.org.
                # Most likely the password to said account is configured incorrectly
                return render(request, "kulukorvaus.html", {"error": True})

            # Successfull form submission - render page displaying
            # info and pdf download link.
            return render(
                request,
                "kulukorvaus.html",
                {"done": True, "perustiedot_id": model_perustiedot.id},
            )
        else:
            # Form submission contained errors. Return status code 599
            # (599 is not specified in any RFC). The status code is captured
            # in javascript and form errors are displayed without
            # refreshing the page.
            return render(
                request,
                "kulukorvaus_forms.html",
                {"form_perustiedot": form_perustiedot, "formset_kulu": formset},
                status=599,
            )
    else:
        # Generate empty forms and display them to the user.
        # Initial GET request to this view triggers ends up here.
        form_perustiedot = KulukorvausPerustiedotForm()
        formset = KulukorvausFormset()
        return render(
            request,
            "kulukorvaus.html",
            {"form_perustiedot": form_perustiedot, "formset_kulu": formset},
        )


def send_email(user, perustiedot_id, template, email_to):
    """Informs the user or rahastonhoitaja, by email, of successful kulukorvaus submission.

    Args:
        user: Django user
        perustiedot_id: id of KulukorvausPerustiedot model

    Returns:
      Nothing, sends an email to the right user.
    """
    # Passing the model_perustiedot object straight from main_form
    # Doesn't work. Has something to do with it being in memory still
    # and not having the pdf file attached yet.
    model_perustiedot = KulukorvausPerustiedot.objects.get(id=perustiedot_id)

    # This fetches all the Kulukorvaus objects whose 'info' foreign key
    # attribute is the KulukorvausPerustiedot object obtained above.
    models_kulukorvaukset = model_perustiedot.kulukorvaus_set.all()
    subject = f"Prodeko kulukorvaus - {user.first_name} {user.last_name}"
    text_content = render_to_string(
        template,
        {
            "user": user,
            "model_perustiedot": model_perustiedot,
            "models_kulukorvaukset": models_kulukorvaukset,
        },
    )
    email_to = email_to
    from_email = settings.DEFAULT_FROM_EMAIL
    msg = EmailMultiAlternatives(subject, text_content, from_email, [email_to])

    filename = model_perustiedot.pdf_filename()

    # TODO: No html alternative for now...
    # msg.attach_alternative(html_content, "text/html")
    msg.attach(filename, model_perustiedot.pdf.file.read(), "application/jpg")
    msg.send()
