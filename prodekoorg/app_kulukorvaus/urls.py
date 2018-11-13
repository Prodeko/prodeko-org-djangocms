from django.conf.urls import url
from django.utils.translation import ugettext_lazy as _

from .views import main_form, download_kulukorvaus_pdf

app_name = 'app_kulukorvaus'
urlpatterns = [
    url(_(r'^reimbursement/$'), main_form, name='kulukorvaus'),
    url(r'download-kulukorvaus/(?P<perustiedot_id>[0-9]+)$', download_kulukorvaus_pdf, name='download_kulukorvaus'),
]
