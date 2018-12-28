import datetime
import os
from shutil import rmtree
from unittest.mock import MagicMock

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.test import TestCase

from ..models import Dokumentti

tmp_media_dir = '/tmp/django_test'
# Creates a temporary folder for test file uploads
if not os.path.exists(tmp_media_dir):
    os.makedirs(tmp_media_dir)
settings.MEDIA_ROOT = tmp_media_dir

GDRIVE_ID = '1GUkGy5KDJ7HG9DNbbjUELs_KEBUcE-oV'


class TestData(TestCase):
    """Common test data for app_poytakirjat used across
    test_forms.py, test_models.py and test_views.py

    Args:
        TestCase: https://docs.djangoproject.com/en/dev/topics/testing/tools/#testcase.
    """

    @classmethod
    def setUpTestData(cls):
        # Create a user
        User = get_user_model()
        cls.test_user1 = User.objects.create_user(email='test1@test.com', password='Ukc55Has-@')

        # Create superuser
        cls.test_user2 = User.objects.create_superuser(email='test2@test.com', password='q"WaXkcB>7')

        cls.file_mock_pdf = MagicMock(spec=File, name='FileMock')
        cls.file_mock_pdf.name = 'test_document.pdf'

        cls.test_dokumentti_model = Dokumentti.objects.create(gdrive_id=GDRIVE_ID,
                                                              name='1_1.1.2019',
                                                              number=1,
                                                              date=datetime.date.today(),
                                                              doc_file=cls.file_mock_pdf,
                                                              )

    def tearDown(self):
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)
