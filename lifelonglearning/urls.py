from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^lifelonglearning/(?P<pk>\d+)/$', coursepage, name='coursepage'),
]
