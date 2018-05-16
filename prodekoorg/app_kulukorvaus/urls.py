from django.conf.urls import url
from .views import render_kulukorvaus

app_name = 'app_kulukorvaus'
urlpatterns = [
    url(r'kulukorvaus/$', render_kulukorvaus, name='kulukorvaus'),
]
