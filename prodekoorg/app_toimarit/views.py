from django.http import HttpResponse
from .models import Toimari
from django.conf.urls import url
from django.contrib import admin, messages
from django.core.files import File
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
import csv
import io

from prodekoorg.app_toimarit.models import *

# Create your views here.

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
            #Hallituskohtaiset
            nextRow.virka_eng = line[4]
            nextRow.puhelin = line[5]
            nextRow.sahkoposti = line[6]
            nextRow.save()
        messages.add_message(request, messages.SUCCESS, 'CSV-tiedosto ladattu onnistuneesti')
    except:
        messages.add_message(request, messages.ERROR, 'Virhe tiedostoa ladattaessa')
    return redirect('../../admin/')