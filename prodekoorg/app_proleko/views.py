import random
from .models import Lehti, Post, Ad
from django.contrib.auth.decorators import login_required
from .models import Lehti, Post
from collections import OrderedDict
from itertools import groupby
from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
<< << << < HEAD
== == == =
>>>>>> > Implement Ads model/logic/style

COLORS = [
    "#FF8552",
    "#E6E6E6",
    "#FBB13C",
    "#D81159",
    "#8F2D56",
    "#FFDBB5",
    "#218380",
    "#B7C3F3",
    "#CF1259",
    "#DDE392",
    "#78E0DC",
    "#fcba03",
    "#ff0062",
    "#ffdd00",
    "#ff6600",
    "#0095ff",
    "#00ff99",
    "#07d100",
    "#00e5ff",
]


@login_required
def posts(request):
    posts = Post.objects.all().order_by('-timestamp')
    posts_dict = posts.values()
    ads = list(Ad.objects.all())
    random.shuffle(ads)

    for post in posts_dict:
        post["type"] = "post"
        post["get_thumbnail_image"] = posts.get(
            pk=post["id"]).get_thumbnail_image()
        post["total_likes"] = posts.get(pk=post["id"]).total_likes()
        post["get_date"] = posts.get(pk=post["id"]).get_date()
        color1 = random.choice(COLORS)
        post["color1"] = color1
        color2 = random.choice(COLORS)
        while color2 == color1:
            color2 = random.choice(COLORS)
        post["color2"] = color2

    l = list(posts_dict)
    for i in range(len(ads)):
        # After three first posts, every 5 posts
        # with index correction i (list changes on every append)
        l.insert(3 + i * 5 + i, ads[i])

    return render(request, "posts.html", {"posts": l})


@login_required
def post(request, post_id):
    post = Post.objects.get(pk=post_id)
    user_id = request.user.id
    has_liked = request.user.post_set.filter(id=post_id).exists()
    return render(request, "post.html", {"post": post, "has_liked": has_liked})


@login_required
def like(request, post_id, user_id):
    if request.method == "POST" and request.is_ajax():
        post = Post.objects.get(pk=post_id)
        if request.POST.get("is_liked") == "true":
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        post.save()
        return JsonResponse({"total_likes": post.total_likes()})
    else:
        return HttpResponseBadRequest


@login_required
def archives(request):
    issues = list(Lehti.objects.all())
    grouped = {}
    for issue in issues:
        if issue.year in grouped:
            grouped[issue.year] = sorted(
                grouped[issue.year] + [issue], key=lambda x: x.issue
            )
        else:
            grouped[issue.year] = [issue]
    return render(
        request,
        "archives.html",
        {"magazines": OrderedDict(sorted(grouped.items(), reverse=True))},
    )
