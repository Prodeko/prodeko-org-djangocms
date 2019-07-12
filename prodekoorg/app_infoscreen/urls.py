from django.urls import include, re_path
from .views_api import SlidesList, now

app_name = "app_infoscreen"
urlpatterns = [
    re_path(r"^api/slides/$", SlidesList.as_view()),
    re_path(r"^api/time/$", now),
]
