from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import HallituksenJasen, Jaosto, Toimari


class TestData(TestCase):
    """Common test data for app_toimarit used across
    test_models.py and test_views.py

    Args:
        TestCase: https://docs.djangoproject.com/en/dev/topics/testing/tools/#testcase.
    """

    fixtures = ["test_users.json"]

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
