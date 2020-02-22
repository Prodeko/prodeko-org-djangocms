import tempfile
from unittest.mock import MagicMock

from cms.api import create_page
from cms.constants import TEMPLATE_INHERITANCE_MAGIC
from cms.test_utils.testcases import CMSTestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File

from ..models import Kulukorvaus, KulukorvausPerustiedot


class TestData(CMSTestCase):
    """Common test data for app_kulukorvaus used across
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
            title="kulukorvaus",
            template=TEMPLATE_INHERITANCE_MAGIC,
            language="fi",
            created_by=cls.test_user2,
            published=True,
            login_required=True,
            apphook="KulukorvausApphook",
            apphook_namespace="app_kulukorvaus",
        )

        cls.file_mock_pdf = MagicMock(spec=File, name="FileMock")
        cls.file_mock_pdf.name = "test.pdf"

        cls.file_mock_jpg = MagicMock(spec=File, name="FileMock")
        cls.file_mock_jpg.name = "test.jpg"

        cls.test_perustiedot_model = KulukorvausPerustiedot.objects.create(
            pk=1,
            created_by_user=cls.test_user1,
            created_by="webbitiimi",
            email="webbitiimi@prodeko.org",
            phone_number="999888777666",
            bank_number="FI239482340924092",
            bic="SPANKKI",
            sum_overall=1234,
            additional_info="Some additional info.",
            pdf=cls.file_mock_pdf,
        )

        cls.test_kulukorvaus_model = Kulukorvaus.objects.create(
            pk=1,
            info=cls.test_perustiedot_model,
            target="Testing",
            explanation="Making sure that everything works as expected!",
            sum_euros=99.991,
            additional_info="Some additional info.",
            receipt=cls.file_mock_jpg,
        )
