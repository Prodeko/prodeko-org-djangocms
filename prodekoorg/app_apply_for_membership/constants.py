from django.conf import settings

MAILING_LIST_PRODEKO = (
    "jasenet@prodeko.org" if not settings.DEBUG else "test@prodeko.org"
)

MAILING_LIST_PORA = (
    "jasenet@raittiusseura.org" if not settings.DEBUG else "test@raittiusseura.org"
)
