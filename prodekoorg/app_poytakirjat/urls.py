from django.conf.urls import url
from . import views

app_name = 'app_poytakirjat'
urlpatterns = [
    url(r'^dokumentit', views.docs, name='documents'),
]
