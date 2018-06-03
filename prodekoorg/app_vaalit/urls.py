from django.conf.urls import url
from .views import main_view, question_form

app_name = 'app_vaalit'
urlpatterns = [
    url(r'vaalit/$', main_view, name='vaalit'),
    url(r'vaalit/kysymys$', question_form, name='question_form'),
]
