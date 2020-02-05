import csv
import io
from datetime import datetime

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from filer.models.filemodels import File
from filer.settings import FILER_IMAGE_MODEL
from filer.utils.loader import load_model

from .models import HallituksenJasen, Jaosto, Toimari

Image = load_model(FILER_IMAGE_MODEL)


@staff_member_required
@csrf_protect
def postcsv(request):
    """Handle a CSV POST request and create new Guild Official objects.

    Args:
        request: HttpRequest object from Django.

    Returns:
        If user is logged in and has staff permissions, they will be rediricted to admin home.
        Otherwise they will be redirected to login page.
    """

    try:
        csv_file = request.FILES["file"]
        decoded_file = csv_file.read().decode("utf-8")
        io_string = io.StringIO(decoded_file)
        for line in csv.reader(io_string, delimiter=";", quotechar="|"):
            nextRow = Toimari()
            firstname = line[0]
            lastname = line[1]
            position = line[2]
            section = line[3]
            year = int(line[4])

            # If toimari already exists, don't create a new one
            if not Toimari.objects.filter(
                firstname=firstname,
                lastname=lastname,
                position=position,
                section__name=section,
                year=year,
            ):
                nextRow.firstname = firstname
                nextRow.lastname = lastname
                nextRow.position = position
                nextRow.section = Jaosto.objects.get_or_create(name=section)[0]
                nextRow.year = year

                # The images have to be uploaded to filer before uploading the csv
                image = Image.objects.filter(
                    original_filename__startswith=f"{firstname}_{lastname}",
                    folder__name__contains=str(year),
                ).first()

                if not image:
                    image = Image.objects.get(
                        original_filename__startswith=f"anonymous_prodeko",
                    )

                nextRow.photo = image
                nextRow.save()
        messages.add_message(request, messages.SUCCESS, _("CSV imported successfully."))
    except Exception as e:
        messages.add_message(
            request, messages.ERROR, _("Error downloading CSV: {}".format(e))
        )
    return redirect("../")


def list_current_guildofficials(request):
    """Fetch all Guild Official objects and display them on a page.

    Args:
        request: HttpRequest object from Django.

    Returns:
        A Django TemplateResponse object that renders an html template.
    """

    guildofficials = Toimari.objects.select_related("section").filter(
        year=str(datetime.now().year)
    )
    sections = set([o.section for o in guildofficials])

    context = {"guildofficials": guildofficials, "sections": sections}
    return render(request, "current_guildofficials.html", context)


def list_old_guildofficials(request):
    pass


def list_current_boardmembers(request):
    """Fetch all Board Member objects and display them on a page.

    Args:
        request: HttpRequest object from Django.

    Returns:
        A Django TemplateResponse object that renders an html template.
    """

    boardmembers = HallituksenJasen.objects.get(year=datetime.now().year)
    context = {"boardmembers": boardmembers}
    return render(request, "current_board.html", context)


def list_old_boardmembers(request):
    pass
