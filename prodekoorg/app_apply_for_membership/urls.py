from django.urls import re_path
from django.utils.translation import ugettext_lazy as _

from .views import main_form

app_name = "app_apply_for_membership"
urlpatterns = [re_path(_(r"^apply/$"), main_form, name="apply")]
