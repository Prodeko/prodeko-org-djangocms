from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.urls import path
from django.utils.translation import gettext_lazy as _
from tiedotteet.backend import views, views_api


@apphook_pool.register
class TiedotteetApphook(CMSApp):
    app_name = "tiedotteet"
    name = _("Weekly bulletin application")

    def get_urls(self, page=None, language=None, **kwargs):
        return [
            path("", views.index, name="index"),
            path("cp/", views.control_panel, name="cp"),
            path("cp/messages/<pk>/edit/", views.edit_message, name="edit_message"),
            path(
                "cp/messages/<pk>/delete/", views.delete_message, name="delete_message",
            ),
            path("cp/messages/<pk>/hide/", views.hide_message, name="hide_message"),
            path(
                "cp/messages/<filter>/<category>/",
                views.control_messages,
                name="control_messages",
            ),
            path("cp/categories/", views.categories, name="categories"),
            path("cp/tags/", views.tags, name="tags"),
            path("cp/tags/<pk>/delete/", views.delete_tag, name="delete_tag"),
            path("cp/categories/new/", views.new_category, name="new_category"),
            path("toc/", views.toc, name="toc"),
            path("api/content/", views_api.ContentList.as_view()),
        ]
