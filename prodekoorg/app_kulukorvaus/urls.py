from django.urls import re_path
from .views import download_kulukorvaus_pdf, main_form
from django.utils.translation import ugettext_lazy as _

app_name = "app_kulukorvaus"
urlpatterns = [
    re_path(
        r"download-kulukorvaus/(?P<perustiedot_id>[0-9]+)$",
        download_kulukorvaus_pdf,
        name="download_kulukorvaus",
    ),
    re_path(_(r"^reimbursement/$"), main_form, name="kulukorvaus"),
]
