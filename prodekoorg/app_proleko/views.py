from collections import OrderedDict
from itertools import groupby
from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from .models import Lehti, Post


def posts(request):
    posts = Post.objects.all()
    return render(request, "posts.html", {"posts": posts})


def post(request, post_id):
    post = Post.objects.get(pk=post_id)
    user_id = request.user.id
    has_liked = request.user.post_set.filter(id=post_id).exists()
    return render(request, "post.html", {"post": post, "has_liked": has_liked})


def like(request, post_id, user_id):
    if request.method == "POST" and request.is_ajax():
        post = Post.objects.get(pk=post_id)
        if (request.POST.get('is_liked') == "true"):
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        post.save()
        return JsonResponse({'total_likes': post.total_likes()})
    else:
        return HttpResponseBadRequest


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
