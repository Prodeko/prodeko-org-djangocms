from django.conf.urls import url
from .views import main_view, EhdokasDeleteView, EhdokasUpdateView, delete_kysymys_view

app_name = 'app_vaalit'
urlpatterns = [
    url(r'vaalit/$', main_view, name='vaalit'),
    url(r'vaalit/delete-kysymys/(?P<pk>\d+)/$', delete_kysymys_view, name='delete_kysymys'),
    url(r'vaalit/delete-ehdokas/(?P<pk>\d+)/$', EhdokasDeleteView.as_view(), name='delete_ehdokas'),
    url(r'vaalit/update-ehdokas/(?P<pk>\d+)/$', EhdokasUpdateView.as_view(), name='update_ehdokas'),
]
