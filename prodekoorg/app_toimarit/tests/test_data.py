from cms.test_utils.testcases import CMSTestCase
from django.contrib.auth import get_user_model
from prodekoorg.app_utils.tests.test_utils import CommonTestData
from sekizai.context import SekizaiContext

from ..models import HallituksenJasen, Jaosto, Toimari


class TestData(CMSTestCase, CommonTestData):
    """Common test data for app_toimarit tests.

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

        cls.test_jaosto1 = Jaosto.objects.create(name="Test1")
        cls.test_jaosto2 = Jaosto.objects.create(name="Test2")

        cls.test_toimari1 = Toimari.objects.create(
            firstname="John",
            lastname="Doe",
            position="Webbitiimi",
            section=cls.test_jaosto1,
            year=2019,
        )

        cls.test_hallituksenjasen1 = HallituksenJasen.objects.create(
            firstname="John",
            lastname="Doe",
            position_fi="Puheenjohtaja",
            position_en="Chairman",
            mobilephone="000123123",
            email="puheenjohtaja@test.com",
            year=2020,
        )

        super(TestData, cls).setUpTestData()
