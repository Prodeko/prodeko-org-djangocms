from django.urls import re_path

from tiedotteet.backend import views, views_api

app_name = "tiedotteet"
urlpatterns = [
    re_path(r"^$", views.index, name="index"),
    re_path(r"^cp/$", views.control_panel, name="cp"),
    re_path(
        r"^cp/messages/(?P<pk>\d+)/edit/$", views.edit_message, name="edit_message"
    ),
    re_path(
        r"^cp/messages/(?P<pk>\d+)/delete/$",
        views.delete_message,
        name="delete_message",
    ),
    re_path(
        r"^cp/messages/(?P<pk>\d+)/hide/$", views.hide_message, name="hide_message"
    ),
    re_path(
        r"^cp/messages/(?P<filter>\w+)/(?P<category>\w+)/$",
        views.control_messages,
        name="control_messages",
    ),
    re_path(r"^cp/categories/$", views.categories, name="categories"),
    re_path(r"^cp/tags/$", views.tags, name="tags"),
    re_path(r"^cp/tags/(?P<pk>\d+)/delete/$", views.delete_tag, name="delete_tag"),
    re_path(r"^cp/categories/new/$", views.new_category, name="new_category"),
    re_path(r"^toc/", views.toc, name="toc"),
    re_path(r"^api/content/$", views_api.ContentList.as_view()),
]
