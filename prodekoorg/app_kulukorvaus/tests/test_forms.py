from django.core.files.uploadedfile import SimpleUploadedFile

from ..forms import KulukorvausForm, KulukorvausPerustiedotForm
from .test_data import TestData


class KulukorvausPerustiedotFormTest(TestData):
    """Tests for KulukorvausPerustiedotForm."""

    def test_kulukorvaus_perustiedot_form_valid(self):
        form_data = {
            "id": 1,
            "created_by_user": "webbitiimi@prodeko.org",
            "created_by": "Mediakeisari",
            "email": "webbitiimi@prodeko.org",
            "phone_number": "123456789",
            "bank_number": "FI21 1234 5600 0007 85",
            "bic": "Nordea",
            "sum_overall": 1.51,
            "additional_info": "Tämä on testi!",
        }
        file_data = {"pdf": SimpleUploadedFile("test.pdf", b"a")}
        form = KulukorvausPerustiedotForm(data=form_data, files=file_data)
        self.assertTrue(form.is_valid())

    def test_kulukorvaus_form_invalid_multiple(self):
        form_data = {
            "id": 1,
            "created_by_user": "webbitiimi@prodeko.org",
            "created_by": "",
            "email": "invalid",
            "phone_number": "",
            "bank_number": "",
            "bic": "FALSEBIC",
            "sum_overall": 1.511,
            "additional_info": "Tämä on testi!",
        }
        form = KulukorvausPerustiedotForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)
        self.assertTrue(form["created_by"].errors)
        self.assertTrue(form["email"].errors)
        self.assertTrue(form["phone_number"].errors)
        self.assertTrue(form["bank_number"].errors)
        self.assertTrue(form["bic"].errors)
        self.assertTrue(form["sum_overall"].errors)


class KulukorvausFormTest(TestData):
    """Tests for KulukorvausForm."""

    def test_kulukorvaus_form_valid(self):
        form_data = {
            "info": 1,
            "target": "Testing",
            "explanation": "Making sure that everything works as expected!",
            "sum_euros": 12.39,
            "additional_info": "Tämä on testi!",
            "receipt": self.file_mock_jpg,
        }
        file_data = {"receipt": SimpleUploadedFile("test.jpg", b"a")}
        form = KulukorvausForm(data=form_data, files=file_data)
        self.assertTrue(form.is_valid())

    def test_kulukorvaus_form_invalid_multiple(self):
        form_data = {
            "info": 1,
            "target": "",
            "explanation": "",
            "sum_euros": 12.391,
            "additional_info": "",
        }
        form = KulukorvausForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 4)
        self.assertTrue(form["target"].errors)
        self.assertTrue(form["explanation"].errors)
        self.assertTrue(form["sum_euros"].errors)
        self.assertTrue(form["receipt"].errors)
