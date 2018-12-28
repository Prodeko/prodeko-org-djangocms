from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import HallituksenJasen, Jaosto, Toimari


class TestData(TestCase):
    """Common test data for app_toimarit used across
    test_forms.py, test_models.py and test_views.py

    Args:
        TestCase: https://docs.djangoproject.com/en/dev/topics/testing/tools/#testcase.
    """

    @classmethod
    def setUpTestData(cls):

        User = get_user_model()
        cls.test_user1 = User.objects.create_user(email='test1@test.com', password='Ukc55Has-@')
        cls.test_user1.is_staff = True
        cls.test_user1.save()
        cls.test_user2 = User.objects.create_user(email='test2@test.com', password='q"WaXkcB>7')

        cls.test_jaosto1 = Jaosto.objects.create(name='Test1')
        cls.test_jaosto2 = Jaosto.objects.create(name='Test2')

        cls.test_toimari1 = Toimari.objects.create(firstname='John',
                                                   lastname='Doe',
                                                   position='Webbitiimi',
                                                   section=cls.test_jaosto1)

        cls.test_hallituksenjasen1 = HallituksenJasen.objects.create(firstname='John',
                                                                     lastname='Doe',
                                                                     position='Puheenjohtaja',
                                                                     position_eng='Chairman',
                                                                     section=cls.test_jaosto2,
                                                                     mobilephone='000123123',
                                                                     email='puheenjohtaja@test.com')
