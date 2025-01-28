import os

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.utils import override_settings
from django.urls import reverse

from ..models import HallituksenJasen, Jaosto, Toimari
from .test_data import TestData

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
csv_toimari_test = open(os.path.join(__location__, "csv_toimari_test.csv"), "rb")
csv_hallitus_test = open(os.path.join(__location__, "csv_hallitus_test.csv"), "rb")


class AppToimaritViewTest(TestData):
    """Tests for views in the app_toimarit app."""

    def test_hallitus_postcsv_redirect_if_not_logged_in(self):
        """
        Tests redirect to login page if the postcsv url is accessed
        and the user is not logged in.
        """

        response = self.client.get(reverse("admin:hallitus_postcsv"))
        self.assertRedirects(
            response,
            "/en/admin/login/?next=/en/admin/app_toimarit/hallituksenjasen/postcsv",
        )

    def test_hallitus_postcsv_if_not_correct_permissions(self):
        """
        Tests redirect to login page if the postcsv page is
        accessed and the user is not an admin.
        """

        self.client.login(email="test1@test.com", password="test1salasana")

        response = self.client.get(reverse("admin:hallitus_postcsv"))
        self.assertRedirects(
            response,
            "/en/admin/login/?next=/en/admin/app_toimarit/hallituksenjasen/postcsv",
        )

    def test_hallitus_postcsv_correct_import_and_permissions(self):
        """
        Tests that hallitus postcsv view works correctly.
        """

        self.client.login(email="test2@test.com", password="test2salasana")

        test_data = {
            "file": SimpleUploadedFile(
                "csv_hallitus_test.csv", csv_hallitus_test.read()
            )
        }

        response = self.client.post(
            reverse("admin:hallitus_postcsv"), data=test_data, follow=True
        )

        hallituksenjasen = HallituksenJasen.objects.get(firstname="Arnold")

        self.assertEqual(hallituksenjasen.firstname, "Arnold")
        self.assertEqual(hallituksenjasen.lastname, "Norsumäki")
        self.assertEqual(hallituksenjasen.position_fi, "Kirjeenvaihtaja")
        self.assertEqual(hallituksenjasen.position_en, "Letter Exchanger")
        self.assertEqual(hallituksenjasen.year, 1966)
        self.assertEqual(hallituksenjasen.mobilephone, "+358111222333")
        self.assertEqual(hallituksenjasen.email, "arnold.norsumäki@prodeko.org")
        self.assertEqual(hallituksenjasen.telegram, "@arska")

        self.assertRedirects(response, ".")

    def test_toimari_postcsv_correct_import_and_permissions(self):
        """
        Tests that toimari postcsv view works correctly.
        """

        self.client.login(email="test2@test.com", password="test2salasana")

        test_data = {
            "file": SimpleUploadedFile("csv_toimari_test.csv", csv_toimari_test.read())
        }

        response = self.client.post(
            reverse("admin:toimari_postcsv"), data=test_data, follow=True
        )

        toimarit = Toimari.objects.all()

        # toimarit[0] is John Doe created in test_data.py
        toimari1 = toimarit[1]
        toimari2 = toimarit[2]

        self.assertEqual(toimari1.firstname, "Test")
        self.assertEqual(toimari1.lastname, "Tester")
        self.assertEqual(toimari1.position, "Keppitiimi")
        self.assertEqual(toimari1.section, Jaosto.objects.get(name="Testijaosto"))
        self.assertEqual(toimari1.year, 2020)

        self.assertEqual(toimari2.firstname, "Test 2")
        self.assertEqual(toimari2.lastname, "Nakkikone")
        self.assertEqual(toimari2.position, "Webbitiimi")
        self.assertEqual(toimari2.section, Jaosto.objects.get(name="Nakkijaosto"))
        self.assertEqual(toimari2.year, 2019)

        self.assertRedirects(response, ".")
