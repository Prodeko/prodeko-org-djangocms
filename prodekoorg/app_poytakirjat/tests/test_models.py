from .test_data import TestData


class DokumenttiModelTest(TestData):
    """Tests for Dokumentti model."""

    def test_gdrive_id_max_length(self):
        max_length = self.test_dokumentti_model._meta.get_field("name").max_length
        self.assertEqual(max_length, 50)

    def test_name_max_length(self):
        max_length = self.test_dokumentti_model._meta.get_field("gdrive_id").max_length
        self.assertEqual(max_length, 99)

    def test_get_absolute_url(self):
        model = self.test_dokumentti_model
        self.assertEqual(model.get_absolute_url(), model.doc_file.url)
