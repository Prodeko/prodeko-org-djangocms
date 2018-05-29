from django.conf.urls import url
from .views import main_view, EhdokasCreateView

app_name = 'app_vaalit'
urlpatterns = [
    url(r'vaalit/$', main_view, name='vaalit'),
    url(r'vaalit/create-ehdokas/$', EhdokasCreateView.as_view(), name='create-ehdokas'),
]
