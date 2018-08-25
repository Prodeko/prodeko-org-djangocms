from django.conf.urls import url
from .views import *

app_name = 'lifelonglearning'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^(?P<pk>\d+)/$', coursepage, name='coursepage'),
]
