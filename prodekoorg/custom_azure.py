from azure.common import AzureMissingResourceHttpError
from django.conf import settings
from django.contrib.staticfiles.storage import ManifestFilesMixin
from storages.backends.azure_storage import AzureStorage


class AzureMediaStorage(AzureStorage):
    account_key = settings.STORAGE_KEY
    azure_container = "media"
    expiration_secs = None
    # This is needed for django-filer
    base_url = "media"


class AzureStaticStorage(ManifestFilesMixin, AzureStorage):
    account_key = settings.STORAGE_KEY
    azure_container = "static"
    expiration_secs = None

    def read_manifest(self):
        """Workaround to make Azure work with Django on the first 'collectstatic'

        See https://github.com/jschneier/django-storages/issues/630 for details.
        """
        try:
            return super(AzureStaticStorage, self).read_manifest()
        except AzureMissingResourceHttpError:
            return None
