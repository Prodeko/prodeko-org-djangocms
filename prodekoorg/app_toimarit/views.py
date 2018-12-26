import csv
import io

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect, render

from .models import HallituksenJasen, Jaosto, Toimari



@staff_member_required(login_url='/login/')
@csrf_protect
def postcsv(request):
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
        messages.add_message(request, messages.SUCCESS, 'CSV-tiedosto ladattu onnistuneesti')
    except:
        messages.add_message(request, messages.ERROR, 'Virhe tiedostoa ladattaessa')
    return redirect('../../admin/')


def list_guildofficials(request):
    guildofficials = Toimari.objects.all()
    sections = Jaosto.objects.all()
    context = {'guildofficials': guildofficials, 'sections': sections}
    return render(request, 'guildofficials.html', context)


def list_boardmembers(request):
    boardmembers = HallituksenJasen.objects.all()
    context = {'boardmembers': boardmembers}
    return render(request, 'board.html', context)
