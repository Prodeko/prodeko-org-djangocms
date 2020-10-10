from datetime import datetime
from unittest.mock import MagicMock

from cms.api import create_page
from cms.constants import TEMPLATE_INHERITANCE_MAGIC
from cms.test_utils.testcases import CMSTestCase
from django.contrib.auth import get_user_model
from django.core.files import File
from prodekoorg.app_utils.tests.test_utils import CommonTestData
from sekizai.context import SekizaiContext

from ..models import Dokumentti

GDRIVE_ID = "1GUkGy5KDJ7HG9DNbbjUELs_KEBUcE-oV"


class TestData(CMSTestCase, CommonTestData):
    """Common test data for app_poytakirjat tests.

    Args:
        CMSTestCase: http://docs.django-cms.org/en/latest/how_to/testing.html.
        CommonTestData: Defined in prodekoorg.app_utils.test.test_utils
    """

    fixtures = ["test_users.json"]
    context = SekizaiContext()

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.test_user1 = User.objects.get(email="test1@test.com")
        cls.test_user2 = User.objects.get(email="test2@test.com")

        cls.another_page = create_page(
            title="kokouspöytäkirjat",
            template=TEMPLATE_INHERITANCE_MAGIC,
            language="fi",
            created_by=cls.test_user2,
            published=True,
            login_required=True,
            apphook="MinutesApphook",
            apphook_namespace="app_poytakirjat",
        )

        cls.file_mock_pdf = MagicMock(spec=File, name="FileMock")
        cls.file_mock_pdf.name = "test_document.pdf"

        cls.test_dokumentti_model1 = Dokumentti.objects.create(
            gdrive_id=GDRIVE_ID,
            name="1_1.1.2019",
            number=1,
            date=datetime.strptime("01.01.2019", "%d.%m.%Y"),
            doc_file=cls.file_mock_pdf,
        )

        cls.test_dokumentti_model2 = Dokumentti.objects.create(
            gdrive_id=GDRIVE_ID,
            name="2_8.1.2020",
            number=2,
            date=datetime.strptime("08.01.2020", "%d.%m.%Y"),
            doc_file=cls.file_mock_pdf,
        )

        super(TestData, cls).setUpTestData()
