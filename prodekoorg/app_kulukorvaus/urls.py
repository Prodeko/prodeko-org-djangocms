from django.conf.urls import url

from .views import main_form

app_name = 'app_kulukorvaus'
urlpatterns = [
    url(r'kulukorvaus/$', main_form, name='kulukorvaus'),
]
