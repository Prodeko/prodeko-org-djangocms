from django.conf.urls import url

from .views import main_form

app_name = 'app_apply_for_membership'
urlpatterns = [
    url(r'apply/$', main_form, name='apply'),
]
