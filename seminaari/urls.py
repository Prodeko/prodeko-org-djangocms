from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import index

app_name = 'seminaari'
urlpatterns = [
    url(r'^$', index, name='index'),
] + staticfiles_urlpatterns()
