from django.urls import include, re_path
from tiedotteet.info import views, views_api

app_name = "tiedotteet"
urlpatterns = [
    # index
    re_path(r"^$", views.index, name="index"),
    # ckeditor
    re_path(r"^ckeditor/", include("ckeditor_uploader.urls")),
    # Control panel
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
    re_path(r"^cp/email/$", views.control_panel_email, name="control_panel_email"),
    re_path(r"^cp/email/send/$", views.send_email, name="send_email"),
    # email and toc templates
    re_path(r"^email/", views.email, name="email"),
    re_path(r"^toc/", views.toc, name="toc"),
    # API
    re_path(r"^api/content/$", views_api.ContentList.as_view()),
]
