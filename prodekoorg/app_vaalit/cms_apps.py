from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.utils.translation import ugettext_lazy as _
from .views import (
    EhdokasCreateView,
    EhdokasDeleteView,
    EhdokasUpdateView,
    delete_kysymys_view,
    main_view,
    mark_as_read,
    update_kysymys_view,
)


@apphook_pool.register
class VaalitApphook(CMSApp):
    app_name = "app_vaalit"
    name = _("Elections application")

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            path("", main_view, name="vaalit"),
            path(
                "delete-question/<int:pk>/", delete_kysymys_view, name="delete_kysymys"
            ),
            path(
                "update-question/<int:pk>/",
                login_required(update_kysymys_view),
                name="update_kysymys",
            ),
            path(
                "delete-nominee/<int:pk>/",
                login_required(EhdokasDeleteView.as_view()),
                name="delete_ehdokas",
            ),
            path(
                "update-nominee/<int:pk>/",
                login_required(EhdokasUpdateView.as_view()),
                name="update_ehdokas",
            ),
            path(
                "mark-read/<int:pk>/", login_required(mark_as_read), name="mark_as_read"
            ),
        ]
