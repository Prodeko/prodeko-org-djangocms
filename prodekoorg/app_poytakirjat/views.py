from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Dokumentti


@login_required
def docs(request):
    """Fetch all Dokumentti objects and display them on a page.

    Args:
        request: HttpRequest object from Django.

    Returns:
        A Django TemplateResponse object that renders a html template.

        If the user isn't logged in, they are redirected to the login url.
    """

    docs = Dokumentti.objects.all().order_by("date")
    iterable = [(str(doc.date.year), doc) for doc in docs]
    context = defaultdict(list)
    for year, doc in iterable:
        context[year].append(doc)
    context = dict(context)
    return render(request, "documents.html", {"context": context})
