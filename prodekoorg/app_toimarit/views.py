import csv
import io

from django.conf.urls import url
from django.contrib import admin, messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from prodekoorg.app_toimarit.models import *
from django.http import JsonResponse
from django.core import serializers

from .models import Toimari


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
            nextRow.jaosto = line[3]
            # Hallituskohtaiset
            nextRow.virka_eng = line[4]
            nextRow.puhelin = line[5]
            nextRow.sahkoposti = line[6]
            nextRow.save()
        messages.add_message(request, messages.SUCCESS, 'CSV-tiedosto ladattu onnistuneesti')
    except:
        messages.add_message(request, messages.ERROR, 'Virhe tiedostoa ladattaessa')
    return redirect('../../admin/')

def list_toimarit(request):
    toimarit = Toimari.objects.filter(sahkoposti="")    #Laiska tapa erotella hallituslaiset toimareista, saa parantaa
    jaostot = Toimari.objects.order_by().values_list('jaosto', flat=True).distinct()
    context = {'toimarit': toimarit, 'jaostot': jaostot}
    #return HttpResponse(data, content_type="application/json")
    return render(request, 'toimarit.html', context)

def list_hallitus(request):
    toimarit = Toimari.objects.exclude(sahkoposti="")   #Laiska tapa erotella hallituslaiset toimareista, saa parantaa
    jaostot = Toimari.objects.order_by().values_list('jaosto', flat=True).distinct()
    context = {'toimarit': toimarit, 'jaostot': jaostot}
    return render(request, 'hallitus.html', context)