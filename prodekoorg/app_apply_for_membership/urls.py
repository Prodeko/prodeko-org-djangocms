from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views import main_form

app_name = 'app_apply_for_membership'
urlpatterns = [
    url(_(r'apply/'), main_form, name='apply'),
]
