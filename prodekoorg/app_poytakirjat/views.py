from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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
    return render(request, 'documents.html', {'context': context})
