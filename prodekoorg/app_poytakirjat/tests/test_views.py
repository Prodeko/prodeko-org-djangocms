import pytest
from django.conf import settings
from django.test.utils import override_settings
from django.urls import reverse

from ..models import Dokumentti
from .test_data import TestData

urlconf = "prodekoorg.urls"


class DokumenttiViewTest(TestData):
    """Tests for views in the app_poytakirjat app."""

    def test_poytakirjat_and_redirect_if_not_logged_in(self):
        """
        Tests redirect to login page if the main poytakirjat page is
        accessed and the user is not logged in.
        """

        response = self.client.get("/en/kokouspoytakirjat/", follow=True)
        self.assertRedirects(response, "/en/login/?next=/en/kokouspoytakirjat/")

    def test_admin_download_not_authorized(self):
        """
        Test documents downloading from admin panel.
        """

        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "fi"})
        self.client.login(email="test1@test.com", password="test1salasana")
        test_data = {"folderID": "1RD-AIF6GuB08wDSFKxNxRZgBu2BtPEli"}
        response = self.client.post(
            reverse("admin:download_docs_from_gsuite"), data=test_data
        )
        self.assertRedirects(
            response,
            "/en/admin/login/?next=/en/admin/app_poytakirjat/dokumentti/download",
        )

    def test_template_renders_correctly(self):
        """
        Test that template renders the correct number of documents.
        """

        self.client.login(email="test1@test.com", password="test1salasana")

        response = self.client.get("/fi/kokouspoytakirjat/")

        self.assertContains(response, "/media/dokumentit/2019", count=1)
        self.assertContains(response, "/media/dokumentit/2020", count=1)

    @pytest.mark.skip(
        reason="This is a long running test. Run if you suspect the G Drive integration is broken."
    )
    def test_admin_download_authorized(self):
        """
        Test documents downloading from admin panel.

        This test may run for a little while as it downloads the
        documents through Google's API to a test database. The test
        database is destroyed after the test run.
        """

        self.client.login(email="test2@test.com", password="test2salasana")
        test_data = {"folderID": "1RD-AIF6GuB08wDSFKxNxRZgBu2BtPEli"}
        response = self.client.post(
            reverse("admin:download_docs_from_gsuite"), data=test_data
        )
        self.assertRedirects(response, "/fi/admin/app_poytakirjat/dokumentti/")
