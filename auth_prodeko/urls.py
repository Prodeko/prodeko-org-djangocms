from django.urls import path
from mozilla_django_oidc.views import OIDCLogoutView

from .oidc.views import OIDCLoginRedirectView
from .views import accept_policies, login_failed, profile

app_name = "auth_prodeko"
urlpatterns = [
    path("profile/", profile, name="profile"),
    path("accept_policies/", accept_policies, name="accept_policies"),
    # Templates, LOGIN_URL and every login_required decorator through it
    # point at these names, so the names stay where they are and the
    # views behind them lead to Keycloak. Passwords belong to the Prodeko
    # account, not to this site.
    path("login/", OIDCLoginRedirectView.as_view(), name="login"),
    path("login-failed/", login_failed, name="login_failed"),
    path("logout/", OIDCLogoutView.as_view(), name="logout"),
]
