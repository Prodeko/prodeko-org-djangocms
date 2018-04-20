from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import render, render_to_response, redirect, HttpResponseRedirect, get_object_or_404, HttpResponse
from django.utils import timezone

from .models import Dokumentti

from collections import defaultdict


#@login_required
def docs(request):
    docs = Dokumentti.objects.all()
    iterable = [(str(doc.date.year), doc) for doc in docs]
    context = defaultdict(list)
    for year, doc in iterable:
        context[year].append(doc)
    context = dict(context)
    return render(request, '../templates/custompages/documents.html', {'context': context})
