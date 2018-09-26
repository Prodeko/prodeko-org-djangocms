from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import main_view, EhdokasDeleteView, EhdokasUpdateView, delete_kysymys_view, update_kysymys_view

app_name = 'app_vaalit'
urlpatterns = [
    url(r'^vaalit/$', main_view, name='vaalit'),
    url(r'^vaalit/delete-kysymys/(?P<pk>\d+)/$', login_required(delete_kysymys_view), name='delete_kysymys'),
    url(r'^vaalit/update-kysymys/(?P<pk>\d+)/$', login_required(update_kysymys_view), name='update_kysymys'),
    url(r'^vaalit/delete-ehdokas/(?P<pk>\d+)/$', login_required(EhdokasDeleteView.as_view()), name='delete_ehdokas'),
    url(r'^vaalit/update-ehdokas/(?P<pk>\d+)/$', login_required(EhdokasUpdateView.as_view()), name='update_ehdokas'),
]
