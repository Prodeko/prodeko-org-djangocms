from django.conf.urls import url
from django.contrib.auth import views as auth_views
from alumnirekisteri.rekisteri import views, views_api
from rest_framework.urlpatterns import format_suffix_patterns
from alumnirekisteri.auth2.forms import LoginForm
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import TemplateView

# prevent logged in users for accessing /login/ url
login_forbidden =  user_passes_test(lambda u: u.is_anonymous(), '/')

urlpatterns = [

    # Admin
    url(r'^admin/profiles/(?P<pk>[0-9]+)/edit/$', views.admin_edit_person_view, name='admin_edit_person_view'),
    url(r'^admin/member-requests/$', views.admin_member_requests, name='admin_member_requests'),
    url(r'^admin/export-data/$', views.admin_export_data, name='admin_export_data'),
    url(r'^admin/export-matrikkeli/$', views.admin_export_matrikkeli, name='admin_export_matrikkeli'),
    url(r'^admin/log/$', views.admin_log, name='admin_log'),
    url(r'^admin/stats/', views.admin_stats, name='admin_stats'),
    url(r'^admin/set_notes/', views.admin_set_notes, name='admin_set_notes'),
    url(r'^admin/', views.admin, name='admin'),

    # Index
    url(r'^$', views.index, name='index'),

    # My profile
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^new-password/$', views.new_password, name='new_password'),
    url(r'^myprofile/$', views.myprofile, name='myprofile'),
    url(r'^myprofile/delete-profile/$', views.delete_profile, name='delete_profile'),

    url(r'^myprofile/add-phone/(?P<person_pk>[0-9]+)$', views.add_phone, name='add_phone'),
    url(r'^myprofile/edit-phone/(?P<pk>[0-9]+)$', views.edit_phone, name='edit_phone'),
    url(r'^myprofile/delete-phone/(?P<pk>[0-9]+)$', views.delete_phone, name='delete_phone'),

    url(r'^myprofile/add-email/(?P<person_pk>[0-9]+)$', views.add_email, name='add_email'),
    url(r'^myprofile/edit-email/(?P<pk>[0-9]+)$', views.edit_email, name='edit_email'),
    url(r'^myprofile/delete-email/(?P<pk>[0-9]+)$', views.delete_email, name='delete_email'),

    url(r'^myprofile/add-skill/(?P<person_pk>[0-9]+)$', views.add_skill, name='add_skill'),
    url(r'^myprofile/edit-skill/(?P<pk>[0-9]+)$', views.edit_skill, name='edit_skill'),
    url(r'^myprofile/delete-skill/(?P<pk>[0-9]+)$', views.delete_skill, name='delete_skill'),

    url(r'^myprofile/add-language/(?P<person_pk>[0-9]+)$', views.add_language, name='add_language'),
    url(r'^myprofile/edit-language/(?P<pk>[0-9]+)$', views.edit_language, name='edit_language'),
    url(r'^myprofile/delete-language/(?P<pk>[0-9]+)$', views.delete_language, name='delete_language'),

    url(r'^myprofile/add-education/(?P<person_pk>[0-9]+)$', views.add_education, name='add_education'),
    url(r'^myprofile/edit-education/(?P<pk>[0-9]+)$', views.edit_education, name='edit_education'),
    url(r'^myprofile/delete-education/(?P<pk>[0-9]+)$', views.delete_education, name='delete_education'),

    url(r'^myprofile/add-work-experience/(?P<person_pk>[0-9]+)$', views.add_work_experience, name='add_work_experience'),
    url(r'^myprofile/edit-work-experience/(?P<pk>[0-9]+)$', views.edit_work_experience, name='edit_work_experience'),
    url(r'^myprofile/delete-work-experience/(?P<pk>[0-9]+)$', views.delete_work_experience, name='delete_work_experience'),

    url(r'^myprofile/add-position-of-trust/(?P<person_pk>[0-9]+)$', views.add_position_of_trust, name='add_position_of_trust'),
    url(r'^myprofile/edit-position-of-trust/(?P<pk>[0-9]+)$', views.edit_position_of_trust, name='edit_position_of_trust'),
    url(r'^myprofile/delete-position-of-trust/(?P<pk>[0-9]+)$', views.delete_position_of_trust, name='delete_position_of_trust'),

    url(r'^myprofile/add-student-activity/(?P<person_pk>[0-9]+)$', views.add_student_activity, name='add_student_activity'),
    url(r'^myprofile/edit-student-activity/(?P<pk>[0-9]+)$', views.edit_student_activity, name='edit_student_activity'),
    url(r'^myprofile/delete-student-activity/(?P<pk>[0-9]+)$', views.delete_student_activity, name='delete_student_activity'),

    url(r'^myprofile/add-volunteer/(?P<person_pk>[0-9]+)$', views.add_volunteer, name='add_volunteer'),
    url(r'^myprofile/edit-volunteer/(?P<pk>[0-9]+)$', views.edit_volunteer, name='edit_volunteer'),
    url(r'^myprofile/delete-volunteer/(?P<pk>[0-9]+)$', views.delete_volunteer, name='delete_volunteer'),

    url(r'^myprofile/add-honor/(?P<person_pk>[0-9]+)$', views.add_honor, name='add_honor'),
    url(r'^myprofile/edit-honor/(?P<pk>[0-9]+)$', views.edit_honor, name='edit_honor'),
    url(r'^myprofile/delete-honor/(?P<pk>[0-9]+)$', views.delete_honor, name='delete_honor'),

    url(r'^myprofile/add-interest/(?P<person_pk>[0-9]+)$', views.add_interest, name='add_interest'),
    url(r'^myprofile/edit-interest/(?P<pk>[0-9]+)$', views.edit_interest, name='edit_interest'),
    url(r'^myprofile/delete-interest/(?P<pk>[0-9]+)$', views.delete_interest, name='delete_interest'),

    url(r'^myprofile/add-family-member/(?P<person_pk>[0-9]+)$', views.add_family_member, name='add_family_member'),
    url(r'^myprofile/edit-family-member/(?P<pk>[0-9]+)$', views.edit_family_member, name='edit_family_member'),
    url(r'^myprofile/delete-family-member/(?P<pk>[0-9]+)$', views.delete_family_member, name='delete_family_member'),

    # Public sites
    url(r'^profiles/(?P<slug>[\w-]+)/', views.public_profile, name='public_profile'),
    url(r'^search/', views.search, name='search'),

    # Auth
    url(r'^login/$', login_forbidden(auth_views.login), {'template_name': 'login.html', 'authentication_form':LoginForm}, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^confirmation/$', views.confirmation, name='confirmation'),
    url(r'^change-password/$', views.change_password, name='change_password'),

    url(r'^password_reset/$', auth_views.password_reset, {'template_name':'password_reset.html'}, name='password_reset'),
    url(r'^password_reset_done/$', auth_views.password_reset_done, {'template_name':'password_reset_done.html'}, name='password_reset_done'),
    url(r'^password_reset_confirm/$', auth_views.password_reset_confirm, {'template_name':'password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^password_reset_complete/$', auth_views.password_reset_complete, {'template_name':'password_reset_complete.html'}, name='password_reset_complete'),
    #url(r'^password_reset_complete/$', auth_views.password_reset_complete, {}, name='password_reset_complete'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, {'template_name':'password_reset_confirm.html'}, name='password_reset_confirm'),

    # API
    url(r'^api/users/$', views_api.UserList.as_view()),
    url(r'^api/persons/$', views_api.PersonList.as_view()),
    url(r'^api/persons/(?P<pk>[0-9]+)$', views_api.PersonDetail.as_view()),

    url(r'^robots.txt$', TemplateView.as_view(template_name='robots.txt', content_type="text/plain")),
]


urlpatterns = format_suffix_patterns(urlpatterns)
