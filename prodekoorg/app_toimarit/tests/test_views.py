import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.utils import override_settings
from django.urls import reverse

from ..models import Jaosto, Toimari
from .test_data import TestData

urlconf = "prodekoorg.app_toimarit.tests.test_urls"

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
test_csv = open(os.path.join(__location__, "test_csv_data.csv"), "rb")


@override_settings(ROOT_URLCONF=urlconf, TESTING=True)
class AppToimaritViewTest(TestData):
    """Tests for views in the app_kulukorvaus app."""

    def test_postcsv_redirect_if_not_logged_in(self):
        """
        Tests redirect to login page if the postcsv url is accessed
        and the user is not logged in.
        """

        response = self.client.get(reverse("admin:hallitus_postcsv"))
        self.assertRedirects(
            response,
            "/fi/admin/login/?next=/fi/admin/app_toimarit/hallituksenjasen/postcsv",
        )

    def test_postcsv_if_not_correct_permissions(self):
        """
        Tests redirect to login page if the postcsv page is
        accessed and the user is not an admin.
        """

        self.client.login(email="test1@test.com", password="test1salasana")

        response = self.client.get(reverse("admin:hallitus_postcsv"))
        self.assertRedirects(
            response,
            "/fi/admin/login/?next=/fi/admin/app_toimarit/hallituksenjasen/postcsv",
        )

    def test_postcsv_correct_import_and_permissions(self):
        self.client.login(email="test2@test.com", password="test2salasana")

        test_data = {"file": SimpleUploadedFile("test_csv_data.csv", test_csv.read())}

        response = self.client.post(
            reverse("admin:toimari_postcsv"), data=test_data, follow=True
        )

        toimari = Toimari.objects.get(firstname="Test")

        self.assertEqual(toimari.firstname, "Test")
        self.assertEqual(toimari.lastname, "Tester")
        self.assertEqual(toimari.position, "Keppitiimi")
        self.assertEqual(toimari.section, Jaosto.objects.get(name="Testijaosto"))
        self.assertEqual(toimari.year, 2020)

        self.assertRedirects(response, ".")
