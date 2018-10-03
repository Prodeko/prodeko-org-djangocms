from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views import main_form

app_name = 'app_kulukorvaus'
urlpatterns = [
    url(_(r'reimbursement/'), main_form, name='kulukorvaus'),
]
