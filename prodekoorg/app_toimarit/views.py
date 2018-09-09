import csv
import io

from django.conf.urls import url
from django.contrib import admin, messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core import serializers
from django.core.files import File
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from prodekoorg.app_toimarit.models import *

from .models import HallituksenJasen, Jaosto, Toimari


@staff_member_required
def postcsv(request):
    try:
        csv_file = request.FILES['file']
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        for line in csv.reader(io_string, delimiter=';', quotechar='|'):
            nextRow = Toimari()
            nextRow.etunimi = line[0]
            nextRow.sukunimi = line[1]
            nextRow.virka = line[2]
            # HUOM! Kaikkien Jaostojen täytyy olla jo luotu ennen CSV-tietojen lataamista
            nextRow.jaosto = Jaosto.objects.get(nimi=line[3])
            nextRow.save()
        messages.add_message(request, messages.SUCCESS, 'CSV-tiedosto ladattu onnistuneesti')
    except:
        messages.add_message(request, messages.ERROR, 'Virhe tiedostoa ladattaessa')
    return redirect('../../admin/')


def list_toimarit(request):
    toimarit = Toimari.objects.all()
    jaostot = Jaosto.objects.all()
    context = {'toimarit': toimarit, 'jaostot': jaostot}
    return render(request, 'toimarit.html', context)


def list_hallitus(request):
    hallituslaiset = HallituksenJasen.objects.all()
    context = {'hallituslaiset': hallituslaiset}
    return render(request, 'hallitus.html', context)
