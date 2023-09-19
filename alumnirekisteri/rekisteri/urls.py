from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test
from django.urls import re_path
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns

from alumnirekisteri.rekisteri import views
from alumnirekisteri.rekisteri import views_api

# prevent logged in users for accessing /login/ url
login_forbidden = user_passes_test(lambda u: u.is_anonymous(), "/")

app_name = "alumnirekisteri"
urlpatterns = [
    # Admin
    re_path(
        r"^admin/profiles/(?P<pk>[0-9]+)/edit/$",
        views.admin_edit_person_view,
        name="admin_edit_person_view",
    ),
    re_path(
        r"^admin/member-requests/$",
        views.admin_member_requests,
        name="admin_member_requests",
    ),
    re_path(r"^admin/export-data/$", views.admin_export_data, name="admin_export_data"),
    re_path(
        r"^admin/export-matrikkeli/$",
        views.admin_export_matrikkeli,
        name="admin_export_matrikkeli",
    ),
    re_path(r"^admin/log/$", views.admin_log, name="admin_log"),
    re_path(r"^admin/stats/", views.admin_stats, name="admin_stats"),
    re_path(r"^admin/set_notes/", views.admin_set_notes, name="admin_set_notes"),
    re_path(r"^admin/", views.admin, name="admin"),
    # Index
    re_path(r"^$", views.index, name="index"),
    # My profile
    re_path(r"^settings/$", views.settings, name="settings"),
    re_path(r"^new-password/$", views.new_password, name="new_password"),
    re_path(r"^myprofile/$", views.myprofile, name="myprofile"),
    re_path(r"^myprofile/status/$", views.membership_status, name="membership_status"),
    re_path(
        r"^myprofile/delete-profile/$", views.delete_profile, name="delete_profile"
    ),
    re_path(
        r"^myprofile/add-phone/(?P<person_pk>[0-9]+)$",
        views.add_phone,
        name="add_phone",
    ),
    re_path(
        r"^myprofile/edit-phone/(?P<pk>[0-9]+)$", views.edit_phone, name="edit_phone"
    ),
    re_path(
        r"^myprofile/delete-phone/(?P<pk>[0-9]+)$",
        views.delete_phone,
        name="delete_phone",
    ),
    re_path(
        r"^myprofile/add-email/(?P<person_pk>[0-9]+)$",
        views.add_email,
        name="add_email",
    ),
    re_path(
        r"^myprofile/edit-email/(?P<pk>[0-9]+)$", views.edit_email, name="edit_email"
    ),
    re_path(
        r"^myprofile/delete-email/(?P<pk>[0-9]+)$",
        views.delete_email,
        name="delete_email",
    ),
    re_path(
        r"^myprofile/add-skill/(?P<person_pk>[0-9]+)$",
        views.add_skill,
        name="add_skill",
    ),
    re_path(
        r"^myprofile/edit-skill/(?P<pk>[0-9]+)$", views.edit_skill, name="edit_skill"
    ),
    re_path(
        r"^myprofile/delete-skill/(?P<pk>[0-9]+)$",
        views.delete_skill,
        name="delete_skill",
    ),
    re_path(
        r"^myprofile/add-language/(?P<person_pk>[0-9]+)$",
        views.add_language,
        name="add_language",
    ),
    re_path(
        r"^myprofile/edit-language/(?P<pk>[0-9]+)$",
        views.edit_language,
        name="edit_language",
    ),
    re_path(
        r"^myprofile/delete-language/(?P<pk>[0-9]+)$",
        views.delete_language,
        name="delete_language",
    ),
    re_path(
        r"^myprofile/add-education/(?P<person_pk>[0-9]+)$",
        views.add_education,
        name="add_education",
    ),
    re_path(
        r"^myprofile/edit-education/(?P<pk>[0-9]+)$",
        views.edit_education,
        name="edit_education",
    ),
    re_path(
        r"^myprofile/delete-education/(?P<pk>[0-9]+)$",
        views.delete_education,
        name="delete_education",
    ),
    re_path(
        r"^myprofile/add-work-experience/(?P<person_pk>[0-9]+)$",
        views.add_work_experience,
        name="add_work_experience",
    ),
    re_path(
        r"^myprofile/edit-work-experience/(?P<pk>[0-9]+)$",
        views.edit_work_experience,
        name="edit_work_experience",
    ),
    re_path(
        r"^myprofile/delete-work-experience/(?P<pk>[0-9]+)$",
        views.delete_work_experience,
        name="delete_work_experience",
    ),
    re_path(
        r"^myprofile/add-position-of-trust/(?P<person_pk>[0-9]+)$",
        views.add_position_of_trust,
        name="add_position_of_trust",
    ),
    re_path(
        r"^myprofile/edit-position-of-trust/(?P<pk>[0-9]+)$",
        views.edit_position_of_trust,
        name="edit_position_of_trust",
    ),
    re_path(
        r"^myprofile/delete-position-of-trust/(?P<pk>[0-9]+)$",
        views.delete_position_of_trust,
        name="delete_position_of_trust",
    ),
    re_path(
        r"^myprofile/add-student-activity/(?P<person_pk>[0-9]+)$",
        views.add_student_activity,
        name="add_student_activity",
    ),
    re_path(
        r"^myprofile/edit-student-activity/(?P<pk>[0-9]+)$",
        views.edit_student_activity,
        name="edit_student_activity",
    ),
    re_path(
        r"^myprofile/delete-student-activity/(?P<pk>[0-9]+)$",
        views.delete_student_activity,
        name="delete_student_activity",
    ),
    re_path(
        r"^myprofile/add-volunteer/(?P<person_pk>[0-9]+)$",
        views.add_volunteer,
        name="add_volunteer",
    ),
    re_path(
        r"^myprofile/edit-volunteer/(?P<pk>[0-9]+)$",
        views.edit_volunteer,
        name="edit_volunteer",
    ),
    re_path(
        r"^myprofile/delete-volunteer/(?P<pk>[0-9]+)$",
        views.delete_volunteer,
        name="delete_volunteer",
    ),
    re_path(
        r"^myprofile/add-honor/(?P<person_pk>[0-9]+)$",
        views.add_honor,
        name="add_honor",
    ),
    re_path(
        r"^myprofile/edit-honor/(?P<pk>[0-9]+)$", views.edit_honor, name="edit_honor"
    ),
    re_path(
        r"^myprofile/delete-honor/(?P<pk>[0-9]+)$",
        views.delete_honor,
        name="delete_honor",
    ),
    re_path(
        r"^myprofile/add-interest/(?P<person_pk>[0-9]+)$",
        views.add_interest,
        name="add_interest",
    ),
    re_path(
        r"^myprofile/edit-interest/(?P<pk>[0-9]+)$",
        views.edit_interest,
        name="edit_interest",
    ),
    re_path(
        r"^myprofile/delete-interest/(?P<pk>[0-9]+)$",
        views.delete_interest,
        name="delete_interest",
    ),
    re_path(
        r"^myprofile/add-family-member/(?P<person_pk>[0-9]+)$",
        views.add_family_member,
        name="add_family_member",
    ),
    re_path(
        r"^myprofile/edit-family-member/(?P<pk>[0-9]+)$",
        views.edit_family_member,
        name="edit_family_member",
    ),
    re_path(
        r"^myprofile/delete-family-member/(?P<pk>[0-9]+)$",
        views.delete_family_member,
        name="delete_family_member",
    ),
    # Public sites
    re_path(
        r"^profiles/(?P<slug>[\w-]+)/", views.public_profile, name="public_profile"
    ),
    re_path(r"^search/", views.search, name="search"),
    # Auth
    re_path(
        r"^login/$",
        login_forbidden(auth_views.LoginView.as_view(template_name="login.html")),
        name="login",
    ),
    re_path(r"^register/$", views.register, name="register"),
    re_path(r"^logout/$", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    re_path(r"^confirmation/$", views.confirmation, name="confirmation"),
    re_path(r"^change-password/$", views.change_password, name="change_password"),
    re_path(
        r"^password_reset/$",
        auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
        name="password_reset",
    ),
    re_path(
        r"^password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    re_path(
        r"^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    re_path(
        r"^reset/done/$",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # API
    re_path(r"^api/webhook/stripe/$", views_api.StripeWebhook.as_view()),
    # re_path(r"^api/users/$", views_api.UserList.as_view()),
    # re_path(r"^api/persons/$", views_api.PersonList.as_view()),
    # re_path(r"^api/persons/(?P<pk>[0-9]+)$", views_api.PersonDetail.as_view()),
    re_path(
        r"^robots.txt$",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]


urlpatterns = format_suffix_patterns(urlpatterns)
