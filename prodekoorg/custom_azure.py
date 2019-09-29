from django.conf import settings
from storages.backends.azure_storage import AzureStorage


class AzureMediaStorage(AzureStorage):
    account_name = "prodekostorage"
    account_key = settings.STORAGE_KEY
    azure_container = "media"
    expiration_secs = None
    # This is needed for django-filer
    base_url = "media"


class AzureStaticStorage(AzureStorage):
    account_name = "prodekostorage"
    account_key = settings.STORAGE_KEY
    azure_container = "static"
    expiration_secs = None
