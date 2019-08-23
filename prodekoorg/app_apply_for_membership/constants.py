from django.conf import settings

MAILING_LIST = "jäsenet@prodeko.org" if not settings.DEBUG else "test@prodeko.org"
