from django.shortcuts import render

from .models import Course


def index(request):
    courses = Course.objects.filter(open=True)
    return render(request, "lifelonglearning.html", {"courses": courses})


def coursepage(request, pk):
    course = Course.objects.get(pk=pk)
    return render(request, "coursepage.html", {"course": course})
