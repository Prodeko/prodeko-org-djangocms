from django.urls import path

from .views_api import SlidesList, now

app_name = "app_infoscreen"
urlpatterns = [
    path("api/slides/", SlidesList.as_view()),
    path("api/time/", now),
]
