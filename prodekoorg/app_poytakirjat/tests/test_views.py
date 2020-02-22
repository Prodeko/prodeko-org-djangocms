import unittest

from django.conf import settings
from django.test.utils import override_settings
from django.urls import reverse

from .test_data import TestData

urlconf = "prodekoorg.urls"


@override_settings(ROOT_URLCONF=urlconf, TESTING=True)
class DokumenttiViewTest(TestData):
    """Tests for views in the app_poytakirjat app."""

    def test_poytakirjat_and_redirect_if_not_logged_in(self):
        """
        Tests redirect to login page if the main poytakirjat page is
        accessed and the user is not logged in.
        """

        response = self.client.get("/fi/kokouspoytakirjat/", follow=True)
        self.assertRedirects(response, "/fi/login/?next=/fi/kokouspoytakirjat/")

    def test_admin_download_not_authorized(self):
        """
        Test documents downloading from admin panel.
        """

        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "fi"})
        self.client.login(email="test1@test.com", password="testi1salasana")
        test_data = {"folderID": "1RD-AIF6GuB08wDSFKxNxRZgBu2BtPEli"}
        response = self.client.post(
            reverse("admin:download_docs_from_gsuite"), data=test_data
        )
        self.assertRedirects(
            response,
            "/en/admin/login/?next=/en/admin/app_poytakirjat/dokumentti/download",
        )

    @unittest.skip(
        "This is a long running test. Run if you suspect the G Drive integration is broken."
    )
    def test_admin_download_authorized(self):
        """
        Test documents downloading from admin panel.

        This test may run for a little while as it downloads the
        documents through google API to a test database. The test
        database is destroyed after the test run.
        """

        self.client.login(email="test2@test.com", password="testi2salasana")
        test_data = {"folderID": "1RD-AIF6GuB08wDSFKxNxRZgBu2BtPEli"}
        response = self.client.post(
            reverse("admin:download_docs_from_gsuite"), data=test_data
        )
        self.assertRedirects(response, "/fi/admin/app_poytakirjat/dokumentti/")
