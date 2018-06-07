from django.conf.urls import url
from .views import main_view

app_name = 'app_vaalit'
urlpatterns = [
    url(r'vaalit/$', main_view, name='vaalit'),
]
