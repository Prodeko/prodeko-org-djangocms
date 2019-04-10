from django.conf.urls import include, url
from tiedotteet.info import views, views_api

app_name = 'tiedotteet'
urlpatterns = [

    # index
    url(r'^$', views.index, name='index'),

    # ckeditor
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    # Control panel
    url(r'^cp/$', views.control_panel, name="cp"),
    url(r'^cp/messages/(?P<pk>\d+)/edit/$', views.edit_message, name="edit_message"),
    url(r'^cp/messages/(?P<pk>\d+)/delete/$', views.delete_message, name="delete_message"),
    url(r'^cp/messages/(?P<pk>\d+)/hide/$', views.hide_message, name="hide_message"),
    url(r'^cp/messages/(?P<filter>\w+)/(?P<category>\w+)/$', views.control_messages, name="control_messages"),
    url(r'^cp/categories/$', views.categories, name='categories'),
    url(r'^cp/tags/$', views.tags, name='tags'),
    url(r'^cp/tags/(?P<pk>\d+)/delete/$', views.delete_tag, name='delete_tag'),
    url(r'^cp/categories/new/$', views.new_category, name='new_category'),
    url(r'^cp/email/$', views.control_panel_email, name="control_panel_email"),
    url(r'^cp/email/send/$', views.send_email, name="send_email"),

    # email and toc templates
    url(r'^email/', views.email, name='email'),
    url(r'^toc/', views.toc, name='toc'),

    # API
    url(r'^api/content/$', views_api.ContentList.as_view())
]
