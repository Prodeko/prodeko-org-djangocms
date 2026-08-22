import pytest
from django.conf import settings
from django.urls import reverse

from .test_data import TestData

urlconf = "prodekoorg.urls"


class DokumenttiViewTest(TestData):
    """Tests for views in the app_poytakirjat app."""

    def test_poytakirjat_redirects_to_login_if_not_logged_in(self):
        """
        Tests redirect to the login page if the main poytakirjat page is
        accessed and the user is not logged in. follow=False: the login
        URL now bounces on to Keycloak, which the test client cannot follow.
        """

        response = self.client.get("/en/kokouspoytakirjat/")
        self.assertRedirects(
            response,
            "/en/login/?next=/en/kokouspoytakirjat/",
            fetch_redirect_response=False,
        )

    def test_admin_download_not_authorized(self):
        """
        Test documents downloading from admin panel.
        """

        self.client.cookies.load({settings.LANGUAGE_COOKIE_NAME: "fi"})
        self.client.force_login(self.test_user1)
        test_data = {"folderID": "1RD-AIF6GuB08wDSFKxNxRZgBu2BtPEli"}
        response = self.client.post(
            reverse("admin:download_docs_from_gsuite"), data=test_data
        )
        self.assertRedirects(
            response,
            "/fi/admin/login/?next=/fi/admin/app_poytakirjat/dokumentti/download",
        )

    def test_template_renders_correctly(self):
        """
        Test that template renders the correct number of documents.
        """

        self.client.force_login(self.test_user1)

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

        self.client.force_login(self.test_user2)
        test_data = {"folderID": "1RD-AIF6GuB08wDSFKxNxRZgBu2BtPEli"}
        response = self.client.post(
            reverse("admin:download_docs_from_gsuite"), data=test_data
        )
        self.assertRedirects(response, "/fi/admin/app_poytakirjat/dokumentti/")
