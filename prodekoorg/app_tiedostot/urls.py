from django.conf.urls import url
import views

app_name = 'app_tiedostot'
urlpatterns = [
    url(r'tiedostot/$', 'views.main', name='tiedostot'),
    url(r'tiedostot/download/(?P<file_name>.+)$', 'views.download'),
]
