from django.core.files.uploadedfile import SimpleUploadedFile
from .test_data import TestData

from ..forms import KulukorvausForm, KulukorvausPerustiedotForm


class KulukorvausPerustiedotFormTest(TestData):
    """Tests for KulukorvausPerustiedotForm."""

    def test_kulukorvaus_perustiedot_form_valid(self):
        form_data = {'id': 1,
                     'created_by_user': 'webbitiimi@prodeko.org',
                     'created_by': 'Mediakeisari',
                     'email': 'webbitiimi@prodeko.org',
                     'position_in_guild': 'H',
                     'phone_number': '123456789',
                     'bank_number': 'FI21 1234 5600 0007 85',
                     'bic': 'NORDEA',
                     'sum_overall': 1.51,
                     'additional_info': 'Tämä on testi!',
                     }
        file_data = {'pdf': SimpleUploadedFile('test.pdf', b'a')}
        form = KulukorvausPerustiedotForm(data=form_data, files=file_data)
        self.assertTrue(form.is_valid())

    def test_kulukorvaus_form_invalid_sum_overall_decimals(self):
        form_data = {'id': 1,
                     'created_by_user': 'webbitiimi@prodeko.org',
                     'created_by': 'Mediakeisari',
                     'email': 'webbitiimi@prodeko.org',
                     'position_in_guild': 'H',
                     'phone_number': '123456789',
                     'bank_number': 'FI21 1234 5600 0007 85',
                     'bic': 'NORDEA',
                     'sum_overall': 1.512,
                     'additional_info': 'Tämä on testi!',
                     }
        file_data = {'pdf': SimpleUploadedFile('test.pdf', b'a')}
        form = KulukorvausPerustiedotForm(data=form_data, files=file_data)
        self.assertFalse(form.is_valid())

    def test_kulukorvaus_form_invalid_email(self):
        form_data = {'id': 1,
                     'created_by_user': 'webbitiimi@prodeko.org',
                     'created_by': 'Mediakeisari',
                     'email': 'invalid',
                     'position_in_guild': 'H',
                     'phone_number': '123456789',
                     'bank_number': 'FI21 1234 5600 0007 85',
                     'bic': 'NORDEA',
                     'sum_overall': 1.51,
                     'additional_info': 'Tämä on testi!',
                     }
        file_data = {'pdf': SimpleUploadedFile('test.pdf', b'a')}
        form = KulukorvausPerustiedotForm(data=form_data, files=file_data)
        self.assertFalse(form.is_valid())

    def test_kulukorvaus_form_invalid_position_in_guild(self):
        form_data = {'id': 1,
                     'created_by_user': 'webbitiimi@prodeko.org',
                     'created_by': 'Mediakeisari',
                     'email': 'webbitiimi@prodeko.org',
                     'position_in_guild': 'A',
                     'phone_number': '123456789',
                     'bank_number': 'FI21 1234 5600 0007 85',
                     'bic': 'NORDEA',
                     'sum_overall': 1.51,
                     'additional_info': 'Tämä on testi!',
                     }
        file_data = {'pdf': SimpleUploadedFile('test.pdf', b'a')}
        form = KulukorvausPerustiedotForm(data=form_data, files=file_data)
        self.assertFalse(form.is_valid())


class KulukorvausFormTest(TestData):
    """Tests for KulukorvausForm."""

    def test_kulukorvaus_form_valid(self):
        form_data = {'info': 1,
                     'target': 'Testing',
                     'explanation': 'Making sure that everything works as expected!',
                     'sum_euros': 12.39,
                     'additional_info': 'Tämä on testi!',
                     'receipt': self.file_mock_jpg,
                     }
        file_data = {'receipt': SimpleUploadedFile('test.jpg', b'a')}
        form = KulukorvausForm(data=form_data, files=file_data)
        self.assertTrue(form.is_valid())

    def test_kulukorvaus_form_invalid_sum_euros_decimals(self):
        form_data = {'info': 1,
                     'target': 'Testing',
                     'explanation': 'Making sure that everything works as expected!',
                     'sum_euros': 12.391,
                     'additional_info': 'Tämä on testi!',
                     }
        file_data = {'receipt': SimpleUploadedFile('test.jpg', b'a')}
        form = KulukorvausForm(data=form_data, files=file_data)
        self.assertFalse(form.is_valid())
