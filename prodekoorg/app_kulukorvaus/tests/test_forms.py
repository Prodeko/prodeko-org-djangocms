import tempfile
from unittest.mock import MagicMock

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from ..forms import KulukorvausForm, KulukorvausPerustiedotForm
from ..models import Kulukorvaus, KulukorvausPerustiedot


class TestData(TestCase):
    @classmethod
    def setUpTestData(cls):
        settings.MEDIAROOT = tempfile.mkdtemp()
        # Create a user
        User = get_user_model()
        cls.test_user1 = User.objects.create_user(email='test1@test.com', password='Ukc55Has-@')
        cls.test_user2 = User.objects.create_user(email='test2@test.com', password='q"WaXkcB>7')

        cls.file_mock_pdf = MagicMock(spec=File, name='FileMock')
        cls.file_mock_pdf.name = 'test.pdf'

        cls.file_mock_jpg = MagicMock(spec=File, name='FileMock')
        cls.file_mock_jpg.name = 'test.jpg'

        cls.test_perustiedot_model = KulukorvausPerustiedot.objects.create(created_by_user=cls.test_user1,
                                                                           created_by='webbitiimi',
                                                                           email='webbitiimi@prodeko.org',
                                                                           position_in_guild='T',
                                                                           phone_number='999888777666',
                                                                           bank_number='FI239482340924092',
                                                                           bic='SPANKKI',
                                                                           sum_overall=1234,
                                                                           additional_info='Some additional info.',
                                                                           pdf=cls.file_mock_pdf,)

        cls.test_kulukorvaus_model = Kulukorvaus.objects.create(info=cls.test_perustiedot_model,
                                                                target='Testing',
                                                                explanation='Making sure that everything works as expected!',
                                                                sum_euros=99.991,
                                                                additional_info='Some additional info.',
                                                                receipt=cls.file_mock_jpg,)


class GeneralTests(TestData):
    def test_download_and_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('app_kulukorvaus:download_kulukorvaus', kwargs={
                                   'perustiedot_id': self.test_perustiedot_model.id}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_download_if_not_correct_permissions(self):
        self.client.login(email='test2@test.com', password='q"WaXkcB>7')
        response = self.client.get(reverse('app_kulukorvaus:download_kulukorvaus', kwargs={
                                   'perustiedot_id': self.test_perustiedot_model.id}))
        self.assertEqual(response.status_code, 403)

    def test_download_correct_permissions(self):
        self.client.login(email='test1@test.com', password='Ukc55Has-@')
        response = self.client.get(reverse('app_kulukorvaus:download_kulukorvaus', kwargs={
                                   'perustiedot_id': self.test_perustiedot_model.id}))
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_reimbursement_if_logged_in(self):
        self.client.login(email='test1@test.com', password='Ukc55Has-@')
        response = self.client.get(reverse('app_kulukorvaus:download_kulukorvaus', kwargs={
                                   'perustiedot_id': 999}))
        self.assertEqual(response.status_code, 404)

    def test_form_submission(self):
        self.client.login(email='test1@test.com', password='Ukc55Has-@')
        data = {
            # management_form data
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',

            # First Kulukorvaus data
            'form-0-sum_euros': '23',
            'form-0-info': None,
            'form-0-explanation': 'Testing',
            'form-0-additional_info': '',
            'form-0-target': 'Test',
            'form-0-receipt': self.file_mock_jpg,

            # Second kulukorvaus data
            'form-1-sum_euros': '9001',
            'form-1-info': None,
            'form-1-explanation': 'Testing',
            'form-1-additional_info': '',
            'form-1-target': 'Test2',
            'form-1-receipt': self.file_mock_jpg
        }

        response = self.client.post(reverse("app_kulukorvaus:kulukorvaus"), data)
        self.assertEqual(response.status_code, 200)


class KulukorvausPerustiedotFormTest(TestData):
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
