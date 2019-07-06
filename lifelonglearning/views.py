from django.shortcuts import render

from .models import Course


def index(request):
    openCourses = Course.objects.filter(open=True)
    pastCourses = Course.objects.filter(open=False)
    return render(request, "lifelonglearning.html", {"openCourses": openCourses, "pastCourses": pastCourses})


def coursepage(request, pk):
    course = Course.objects.get(pk=pk)
    return render(request, "coursepage.html", {"course": course})
