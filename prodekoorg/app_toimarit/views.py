import csv
import io

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect

from .models import HallituksenJasen, Jaosto, Toimari


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
        csv_file = request.FILES['file']
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        for line in csv.reader(io_string, delimiter=';', quotechar='|'):
            nextRow = Toimari()
            nextRow.firstname = line[0]
            nextRow.lastname = line[1]
            nextRow.position = line[2]
            # HUOM! Kaikkien Jaostojen täytyy olla jo luotu ennen CSV-tietojen lataamista
            nextRow.section = Jaosto.objects.get(name=line[3])
            nextRow.save()
        messages.add_message(request, messages.SUCCESS, _('CSV imported successfully.'))
    except Exception as e:
        messages.add_message(request, messages.ERROR, _('Error downloading CSV: {}'.format(e)))
    return redirect('../../admin/')


def list_guildofficials(request):
    """Fetch all Guild Official objects and display them on a page.

    Args:
        request: HttpRequest object from Django.

    Returns:
        A Django TemplateResponse object that renders a html template.
    """

    guildofficials = Toimari.objects.all()
    sections = Jaosto.objects.all()
    context = {'guildofficials': guildofficials, 'sections': sections}
    return render(request, 'guildofficials.html', context)


def list_boardmembers(request):
    """Fetch all Board Member objects and display them on a page.

    Args:
        request: HttpRequest object from Django.

    Returns:
        A Django TemplateResponse object that renders a html template.
    """

    boardmembers = HallituksenJasen.objects.all()
    context = {'boardmembers': boardmembers}
    return render(request, 'board.html', context)
