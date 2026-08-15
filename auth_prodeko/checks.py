"""System checks that stop an unconfigurable production deploy early.

Django runs the system checks as part of migrate and collectstatic, both
of which deploy.sh runs before any traffic reaches the new container, so
an error here fails the deploy at a point where the rollback still
restores a working site.
"""

from django.conf import settings
from django.core.checks import Error, Tags, register

# The settings that have to hold a value for a login to work, and the
# variables.txt keys an operator has to fill in to give them one.
REQUIRED_SETTINGS = (
    ("KEYCLOAK_ISSUER", "ISSUER"),
    ("KEYCLOAK_CLIENT_ID", "CLIENT_ID"),
    ("KEYCLOAK_CLIENT_SECRET", "CLIENT_SECRET"),
)


@register(Tags.security)
def check_keycloak_configured(app_configs, **kwargs):
    """Refuse to run a production site that cannot sign anyone in.

    Every OIDC endpoint URL is an f-string over KEYCLOAK_ISSUER, so an
    empty issuer yields a login link to prodeko.org itself and a CMS 404
    instead of Keycloak, and an empty client id or secret is rejected by
    the provider. None of that is visible to a health check, so without
    this the deploy succeeds and the site quietly has no login.

    Development is left alone: DEBUG is True there, and contributors who
    are not working on authentication run with an empty [KEYCLOAK]
    section.
    """
    if settings.DEBUG:
        return []

    missing = [
        key
        for name, key in REQUIRED_SETTINGS
        if not str(getattr(settings, name, "") or "").strip()
    ]
    if not missing:
        return []

    return [
        Error(
            "Keycloak is not configured, so nobody can sign in: "
            f"{', '.join(missing)} {'is' if len(missing) == 1 else 'are'} empty.",
            hint=(
                "Fill in the [KEYCLOAK] section of "
                "prodekoorg/settings/variables.txt. On the production host "
                "that file is a bind mount rendered by Ansible from the "
                "prodeko_org role in the infra-prodeko repository, so run "
                "that role (ansible-playbook playbooks/prodeko_vm.yml "
                "--tags prodeko_org) and confirm the section is on the host "
                "before deploying again; rendering it does not restart the "
                "container. ISSUER is the realm URL with no trailing slash, "
                "CLIENT_ID is the Keycloak client, and CLIENT_SECRET comes "
                "from that client's Credentials tab by way of the "
                "prodekoorg-keycloak-client-secret Key Vault secret. Values "
                "are read literally: no quotes."
            ),
            id="auth_prodeko.E001",
        )
    ]
