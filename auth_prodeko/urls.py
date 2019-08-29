from django.urls import re_path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .views import profile, accept_policies

app_name = "auth_prodeko"
urlpatterns = [
    re_path(r"^profile/$", profile, name="profile"),
    re_path(r"^accept_policies/$", accept_policies, name="accept_policies"),
    re_path(
        r"^login/$",
        auth_views.LoginView.as_view(template_name="prodeko_login.html"),
        name="login",
    ),
    re_path(r"^logout/$", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    re_path(
        r"^password_change/$",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    re_path(
        r"^password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    re_path(
        r"^password_reset/$",
        auth_views.PasswordResetView.as_view(
            template_name="password_reset_form.html",
            email_template_name="password_reset_html_email.html",
            html_email_template_name="password_reset_html_email.html",
            success_url=reverse_lazy("auth_prodeko:password_reset_done"),
        ),
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
            template_name="password_reset_confirm.html",
            success_url=reverse_lazy("auth_prodeko:password_reset_complete"),
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
]
