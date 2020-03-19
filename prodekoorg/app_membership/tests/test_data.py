import tempfile
from unittest.mock import MagicMock

from cms.api import create_page
from cms.constants import TEMPLATE_INHERITANCE_MAGIC
from cms.test_utils.testcases import CMSTestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import PendingUser


class TestData(CMSTestCase):
    """Common test data for app_membership used across
    test_forms.py, test_models.py and test_views.py

    Args:
        CMSTestCase: http://docs.django-cms.org/en/latest/how_to/testing.html.
    """

    fixtures = ["test_users.json"]
    tmp_dir = None

    @classmethod
    def setUpClass(cls):
        cls.tmp_dir = tempfile.TemporaryDirectory(prefix="mediatest")
        settings.MEDIA_ROOT = cls.tmp_dir.name
        super(TestData, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.tmp_dir = None
        super(TestData, cls).tearDownClass()

    @classmethod
    def setUp(cls):
        User = get_user_model()
        cls.test_user1 = User.objects.get(email="test1@test.com")
        cls.test_user2 = User.objects.get(email="test2@test.com")

        cls.another_page = create_page(
            title="jäsenhakemus",
            template=TEMPLATE_INHERITANCE_MAGIC,
            language="fi",
            created_by=cls.test_user2,
            published=True,
            login_required=True,
            apphook="ApplyForMembershipApphook",
            apphook_namespace="app_membership",
        )

        cls.file_mock_pdf = MagicMock(spec=File, name="FileMock")
        cls.file_mock_pdf.name = "test.pdf"

        cls.file_mock_jpg = MagicMock(spec=File, name="FileMock")
        cls.file_mock_jpg.name = "test.jpg"

        cls.test_pendinguser_model = PendingUser.objects.create(
            pk=1,
            user=None,
            first_name="Mediakeisari",
            last_name="Mediakeisari",
            hometown="Espoo",
            field_of_study="Tuotantotalous",
            email="webbitiimi@prodeko.org",
            start_year=2030,
            language="FI",
            membership_type="TR",
            additional_info="muistakaa tehdä testejä!",
            is_ayy_member="Y",
            receipt=SimpleUploadedFile("test.jpg", b"a"),
            has_accepted_policies=True,
        )
