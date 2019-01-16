import unittest

from django.urls import reverse

from .test_data import TestData


class DokumenttiViewTest(TestData):
    """Tests for views in the app_poytakirjat app."""

    def test_poytakirjat_and_redirect_if_not_logged_in(self):
        """
        Tests redirect to login page if the main poytakirjat page is
        accessed and the user is not logged in.
        """
        response = self.client.get(reverse('app_poytakirjat:documents'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/fi/login/?next=/fi/dokumentit/')

    def test_admin_download_not_authorized(self):
        """
        Test documents downloading from admin panel.
        """
        self.client.login(email='test1@test.com', password='Ukc55Has-@')

        test_data = {
            'folderID': '1RD-AIF6GuB08wDSFKxNxRZgBu2BtPEli'
        }

        response = self.client.post(reverse("download_docs_from_gsuite"), data=test_data)
        self.assertRedirects(response, '/fi/admin/login/?next=/fi/admin/poytakirjat/download')

    @unittest.skip("This is a long running test. Run if you suspect the G Drive integration is broken.")
    def test_admin_download_authorized(self):
        """
        Test documents downloading from admin panel.

        This test may run for a little while as it downloads the
        documents through google API to a test database. The test
        database is destroyed after the test run.
        """
        self.client.login(email='test2@test.com', password='q"WaXkcB>7')

        test_data = {
            'folderID': '1RD-AIF6GuB08wDSFKxNxRZgBu2BtPEli'
        }

        response = self.client.post(reverse("download_docs_from_gsuite"), data=test_data)
        self.assertRedirects(response, '/fi/admin/app_poytakirjat/dokumentti/')
