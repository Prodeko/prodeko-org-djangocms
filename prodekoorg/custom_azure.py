from django.conf import settings
from storages.backends.azure_storage import AzureStorage
from django.contrib.staticfiles.storage import ManifestFilesMixin


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

    def read_manifest(self):
        """Handle a workaround to make Azure work with Django on the first 'collectstatic'
        
           See https://github.com/jschneier/django-storages/issues/630 for details.
        """
        try:
            return super(AzureStaticStorage, self).read_manifest()
        except AzureMissingResourceHttpError:
            return None
