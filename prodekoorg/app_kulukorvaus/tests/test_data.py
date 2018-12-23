import tempfile
from unittest.mock import MagicMock

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.test import TestCase

from ..models import Kulukorvaus, KulukorvausPerustiedot


class TestData(TestCase):
    """Common test data for app_kulukorvaus used across
    test_forms.py, test_models.py and test_views.py

    Args:
    TestCase: https://docs.djangoproject.com/en/dev/topics/testing/tools/#testcase.
    """

    @classmethod
    def setUpTestData(cls):
        # Creates a temporary folder like /tmp/tmp505q_7mi where file uploads go
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
