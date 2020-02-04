from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Tapahtuma


@login_required
def docs(request):
    """Fetch all Tapahtuma objects and display them on a page.

    Args:
        request: HttpRequest object from Django.

    Returns:
        A Django TemplateResponse object that renders an html template.

        If the user isn't logged in, they are redirected to the login url.
    """

    # If the user hasn't accepted Prodeko's privacy policy
    # return a 'policy error' page.
    if not request.user.has_accepted_policies:
        return render(request, "events.html", {"policy_error": True})

    docs = Tapahtuma.objects.all().order_by("-date")
    iterable = [(str(doc.date.year), doc) for doc in docs]
    context = defaultdict(list)
    for year, doc in iterable:
        context[year].append(doc)
    context = dict(context)
    return render(request, "events.html", {"context": context})
