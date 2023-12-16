import oauth2_provider.views as oauth2_views
from django.conf import settings
from django.urls import include, path

from .views import UserDetails
from django.contrib.auth.decorators import user_passes_test

def is_superuser(user):
    return user.email in [email for _, email in settings.ADMINS]

oauth2_superuser_required = user_passes_test(is_superuser)

oauth2_endpoint_views = [
    path("auth", oauth2_views.AuthorizationView.as_view(), name="authorize"),
    path("token", oauth2_views.TokenView.as_view(), name="token"),
    path("revoke-token", oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

# OAuth2 Application Management endpoints
oauth2_endpoint_views += [
    path("applications/", oauth2_superuser_required(oauth2_views.ApplicationList.as_view()), name="list"),
    path(
        "applications/register/",
        oauth2_superuser_required(oauth2_views.ApplicationRegistration.as_view()),
        name="register",
    ),
    path(
        "applications/<pk>/",
        oauth2_superuser_required(oauth2_views.ApplicationDetail.as_view()),
        name="detail",
    ),
    path(
        "applications/<pk>/delete/",
        oauth2_superuser_required(oauth2_views.ApplicationDelete.as_view()),
        name="delete",
    ),
    path(
        "applications/<pk>/update/",
        oauth2_superuser_required(oauth2_views.ApplicationUpdate.as_view()),
        name="update",
    ),
]
# OAuth2 Token Management endpoints
oauth2_endpoint_views += [
    path(
        "authorized-tokens/",
        oauth2_superuser_required(oauth2_views.AuthorizedTokensListView.as_view()),
        name="authorized-token-list",
    ),
    path(
        "authorized-tokens/<pk>/delete/",
        oauth2_superuser_required(oauth2_views.AuthorizedTokenDeleteView.as_view()),
        name="authorized-token-delete",
    ),
]

app_name = "app_oauth"
urlpatterns = [
    path("", include(oauth2_endpoint_views)),
    path("user_details/", UserDetails.as_view()),
]
