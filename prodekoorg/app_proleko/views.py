from collections import OrderedDict
from itertools import groupby
from django.shortcuts import render
from .models import Lehti, Post


def posts(request):
    posts = Post.objects.all()
    return render(request, "posts.html", {"posts": posts})


def post(request, post_id):
    post = Post.objects.get(pk=post_id)
    has_liked = False
    return render(request, "post.html", {"post": post, "has_liked": has_liked})


def archives(request):
    issues = list(Lehti.objects.all())
    print(issues)
    grouped = {}
    for issue in issues:
        if (issue.year in grouped):
            grouped[issue.year] = sorted(
                grouped[issue.year] + [issue], key=lambda x: x.issue)
        else:
            grouped[issue.year] = [issue]
    return render(request, "archives.html", {"magazines": OrderedDict(sorted(grouped.items(), reverse=True))})
