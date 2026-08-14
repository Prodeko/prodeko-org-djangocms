from django.urls import path
from mozilla_django_oidc.views import OIDCLogoutView

from .oidc.views import OIDCLoginRedirectView
from .views import accept_policies, profile

app_name = "auth_prodeko"
urlpatterns = [
    path("profile/", profile, name="profile"),
    path("accept_policies/", accept_policies, name="accept_policies"),
    # Names preserved: templates and decorators across the project point
    # here. Passwords now live in the Prodeko account, not on this site.
    path("login/", OIDCLoginRedirectView.as_view(), name="login"),
    path("logout/", OIDCLogoutView.as_view(), name="logout"),
]
