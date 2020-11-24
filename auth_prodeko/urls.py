from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from .views import accept_policies, profile

app_name = "auth_prodeko"
urlpatterns = [
    path("profile/", profile, name="profile"),
    path("accept_policies/", accept_policies, name="accept_policies"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="prodeko_login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="password_reset_form.html",
            email_template_name="password_reset_html_email.html",
            html_email_template_name="password_reset_html_email.html",
            success_url=reverse_lazy("auth_prodeko:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset/confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html",
            success_url=reverse_lazy("auth_prodeko:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
