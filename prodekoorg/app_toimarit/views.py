import csv
import io
from collections import defaultdict
from datetime import datetime

import unidecode
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from filer.settings import FILER_IMAGE_MODEL
from filer.utils.loader import load_model

from .models import HallituksenJasen, Jaosto, Toimari

Image = load_model(FILER_IMAGE_MODEL)


def remove_äö(input_str):
    return unidecode.unidecode(input_str)


def default_to_regular(d):
    if isinstance(d, defaultdict):
        d = {k: default_to_regular(v) for k, v in d.items()}
    return d


@staff_member_required
@csrf_protect
def hallitus_postcsv(request):
    """Handle a CSV POST request and create new HallituksenJasen objects.

    Args:
        request: HttpRequest object from Django.

    Returns:
        Redirects to model admin if user has staff permissions, 
        otherwise redirects to login page.
    """

    try:
        csv_file = request.FILES["file"]
        decoded_file = csv_file.read().decode("utf-8")
        io_string = io.StringIO(decoded_file)
        for line in csv.reader(io_string, delimiter=";", quotechar="|"):
            nextRow = HallituksenJasen()
            firstname = line[0]
            lastname = line[1]
            position_fi = line[2]
            position_en = line[3]
            year = int(line[4])
            mobilephone = line[5]
            email = line[6]
            telegram = line[7]

            # If board member already exists, don't create a new one
            if not HallituksenJasen.objects.filter(
                firstname=firstname,
                lastname=lastname,
                position_fi=position_fi,
                position_en=position_en,
                mobilephone=mobilephone,
                email=email,
                telegram=telegram,
                year=year,
            ):
                nextRow.firstname = firstname
                nextRow.lastname = lastname
                nextRow.position_fi = position_fi
                nextRow.position_en = position_en
                nextRow.mobilephone = mobilephone
                nextRow.email = email
                nextRow.telegram = telegram
                nextRow.year = year

                # The images have to be uploaded to filer before uploading the csv
                image = Image.objects.filter(
                    original_filename__startswith=remove_äö(f"{firstname}_{lastname}"),
                    folder__name__contains=str(year),
                    folder__parent__name__contains="Hallitukset",
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
    return redirect(".")


@staff_member_required
@csrf_protect
def toimari_postcsv(request):
    """Handle a CSV POST request and create new Toimari objects.

    Args:
        request: HttpRequest object from Django.

    Returns:
        Redirects to model admin if user has staff permissions, 
        otherwise redirects to login page.
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
                    original_filename__startswith=remove_äö(f"{firstname}_{lastname}"),
                    folder__name__contains=str(year),
                    folder__parent__name__contains="Toimihenkilöt",
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
    return redirect(".")


def list_current_guildofficials(request):
    """Fetch current guild officials and display them on a page.

    Args:
        request: HttpRequest object from Django.

    Returns:
        A Django TemplateResponse object that renders an html template.
    """

    guildofficials = (
        Toimari.objects.select_related("section")
        .filter(year=datetime.now().year)
        .order_by("-year", "-section", "-lastname")
    )

    context = defaultdict(list)
    for official in guildofficials:
        context[official.section].append(official)

    context = default_to_regular(context)

    return render(request, "current_guildofficials.html", {"context": context})


def list_old_guildofficials(request):
    """Fetch old guild officials and display them on a page.

    Args:
        request: HttpRequest object from Django.

    Returns:
        A Django TemplateResponse object that renders an html template.
    """

    guildofficials = (
        Toimari.objects.select_related("section")
        .filter(year__lt=datetime.now().year)
        .order_by("-year", "-section", "-lastname")
    )

    context = defaultdict(lambda: defaultdict(list))
    for official in guildofficials:
        context[official.year][official.section.name].append(official)

    context = default_to_regular(context)

    return render(request, "old_guildofficials.html", {"context": context})


def list_current_boardmembers(request):
    """Fetch current board members and display them on a page.

    Args:
        request: HttpRequest object from Django.

    Returns:
        A Django TemplateResponse object that renders an html template.
    """

    boardmembers = HallituksenJasen.objects.filter(year=datetime.now().year)

    context = {"boardmembers": boardmembers}

    return render(request, "current_board.html", context)


def list_old_boardmembers(request):
    """Fetch old board members and display them on a page.

    Args:
        request: HttpRequest object from Django.

    Returns:
        A Django TemplateResponse object that renders an html template.
    """

    boardmembers = (
        HallituksenJasen.objects.all()
        .filter(year__lt=datetime.now().year)
        .order_by("-year", "-lastname")
    )

    custom_order = ["Puheenjohtaja", "Varapuheenjohtaja"]
    order = {key: i for i, key in enumerate(custom_order)}
    sorted_boardmembers = sorted(
        boardmembers,
        key=lambda x: order[x.position_fi] if x.position_fi in order else 999,
    )

    context = defaultdict(list)
    for boardmember in sorted_boardmembers:
        context[boardmember.year].append(boardmember)

    context = default_to_regular(context)

    return render(request, "old_boards.html", {"context": context})
