from django.test import override_settings

from .test_data import TestData

# Override settigs to test translations
english = override_settings(
    LANGUAGE_CODE='en',
    LANGUAGES=(('en', 'English'),),
)

finnish = override_settings(
    LANGUAGE_CODE='fi',
    LANGUAGES=(('fi', 'Finnish'),),
)


class DokumenttiModelTest(TestData):
    """Tests for Dokumentti model."""

    def test_gdrive_id_max_length(self):
            max_length = self.test_dokumentti_model._meta.get_field('name').max_length
            self.assertEquals(max_length, 50)

    def test_name_max_length(self):
            max_length = self.test_dokumentti_model._meta.get_field('gdrive_id').max_length
            self.assertEquals(max_length, 99)

    def test_get_absolute_url(self):
        model = self.test_dokumentti_model
        self.assertEquals(model.get_absolute_url(
        ), "{}".format(model.doc_file.url))
