from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from rest_framework.urlpatterns import format_suffix_patterns
from tiedotteet.info import views, views_api

urlpatterns = [

    # index
    url(r'^$', views.index, name='index'),

    # Authentication
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

    # ckeditor
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    # Django Admin
    url(r'^super-admin/', include(admin.site.urls)),

    # Control panel
    url(r'^cp/$', views.control_panel, name="cp"),
    url(r'^cp/messages/(?P<pk>\d+)/edit/$', views.edit_message, name="edit"),
    url(r'^cp/messages/(?P<pk>\d+)/delete/$', views.delete_message),
    url(r'^cp/messages/(?P<pk>\d+)/hide/$', views.hide_message, name="delete"),
    url(r'^cp/messages/(?P<filter>\w+)/(?P<category>\w+)/$', views.control_messages),
    url(r'^cp/categories/$', views.categories, name='categories'),
    url(r'^cp/tags/$', views.tags, name='tags'),
    url(r'^cp/tags/(?P<pk>\d+)/delete/$', views.delete_tag),
    url(r'^cp/categories/new/$', views.new_category, name='new_category'),
    url(r'^cp/email/$', views.control_panel_email, name="control_panel_email"),
    url(r'^cp/email/send/$', views.send_email, name="send_email"),

    # email and toc templates
    url(r'^email/', views.email, name='email'),
    url(r'^toc/', views.toc, name='toc'),

    # API
    url(r'^api/content/$', views_api.ContentList.as_view())
]
