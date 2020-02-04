from django.test import override_settings

from .test_data import TestData

# Override settigs to test translations
english = override_settings(LANGUAGE_CODE="en", LANGUAGES=(("en", "English"),))

finnish = override_settings(LANGUAGE_CODE="fi", LANGUAGES=(("fi", "Finnish"),))


class TapahtumaModelTest(TestData):
    """Tests for Tapahtuma model."""

    def test_gdrive_id_max_length(self):
        max_length = self.test_Tapahtuma_model._meta.get_field("name").max_length
        self.assertEquals(max_length, 50)

    def test_name_max_length(self):
        max_length = self.test_Tapahtuma_model._meta.get_field("gdrive_id").max_length
        self.assertEquals(max_length, 99)

    def test_get_absolute_url(self):
        model = self.test_Tapahtuma_model
        self.assertEquals(model.get_absolute_url(), model.doc_file.url)
