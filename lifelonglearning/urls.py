from django.urls import re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import index, coursepage

app_name = "lifelonglearning"
urlpatterns = [
    re_path(r"^$", index, name="index"),
    re_path(r"^(?P<pk>\d+)/$", coursepage, name="coursepage"),
] + staticfiles_urlpatterns()
