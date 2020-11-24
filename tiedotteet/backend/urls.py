from django.urls import path
from tiedotteet.backend import views, views_api

app_name = "tiedotteet"
urlpatterns = [
    path("", views.index, name="index"),
    path("cp/", views.control_panel, name="cp"),
    path("cp/messages/<pk>/edit/", views.edit_message, name="edit_message"),
    path("cp/messages/<pk>/delete/", views.delete_message, name="delete_message",),
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
