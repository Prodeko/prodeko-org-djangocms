from django.conf import settings

MAILING_LIST = "jasenlista@prodeko.org" if not settings.DEBUG else "test@prodeko.org"
