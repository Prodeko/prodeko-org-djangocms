from django.urls import re_path
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

from .views import (
    EhdokasCreateView,
    EhdokasDeleteView,
    EhdokasUpdateView,
    handle_submit_ehdokas,
    delete_kysymys_view,
    main_view,
    update_kysymys_view,
)

app_name = "app_vaalit"
urlpatterns = [
    re_path(r"^$", main_view, name="vaalit"),
    re_path(
        r"delete-question/(?P<pk>\d+)/",
        delete_kysymys_view,
        name="delete_kysymys",
    ),
    re_path(
        r"^update-question/(?P<pk>\d+)/",
        login_required(update_kysymys_view),
        name="update_kysymys",
    ),
    re_path(
        r"^delete-nominee/(?P<pk>\d+)/",
        login_required(EhdokasDeleteView.as_view()),
        name="delete_ehdokas",
    ),
    re_path(
        r"^update-nominee/(?P<pk>\d+)/",
        login_required(EhdokasUpdateView.as_view()),
        name="update_ehdokas",
    ),
]
