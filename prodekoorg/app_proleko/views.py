from django.shortcuts import render
from .models import Lehti


def posts(request):
    posts = []
    return render(request, "posts", {"posts": posts})


def archives(request):
    lehdet = Lehti.objects.all()
    return render(request, "archives.html", {"magazines": lehdet})
