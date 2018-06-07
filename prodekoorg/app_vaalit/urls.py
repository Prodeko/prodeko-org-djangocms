from django.conf.urls import url
from .views import main_view, kysymys_delete_view

app_name = 'app_vaalit'
urlpatterns = [
    url(r'vaalit/$', main_view, name='vaalit'),
    url(r'vaalit/delete-kysymys/(?P<id>\d+)/$', kysymys_delete_view, name='delete_kysymys'),
]
