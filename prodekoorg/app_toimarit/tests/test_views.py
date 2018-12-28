import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .test_data import TestData
from ..models import Toimari


class AppToimaritViewTest(TestData):
    """Tests for views in the app_kulukorvaus app."""

    def test_postcsv_redirect_if_not_logged_in(self):
        """
        Tests redirect to login page if the postcsv url is accessed
        and the user is not logged in.
        """
        response = self.client.get(reverse('postcsv'))
        self.assertRedirects(response, '/login/?next=/admin/toimarit/postcsv')

    def test_postcsv_if_not_correct_permissions(self):
        """
        Tests redirect to login page if the postcsv page is
        accessed and the user is not an admin.
        """
        self.client.login(email='test2@test.com', password='q"WaXkcB>7')
        response = self.client.get(reverse('postcsv'))
        self.assertRedirects(response, '/login/?next=/admin/toimarit/postcsv')

    def test_postcsv_correct_import_and_permissions(self):
        self.client.login(email='test1@test.com', password='Ukc55Has-@')

        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        test_csv = open(os.path.join(__location__, 'test_csv_data.csv'), "rb")

        test_data = {
            'file': SimpleUploadedFile('test_csv_data.csv', test_csv.read()),
        }

        response = self.client.post(reverse("postcsv"), data=test_data)
        toimari = Toimari.objects.get(firstname="Test")

        self.assertEqual(toimari.firstname, 'Test')
        self.assertEqual(toimari.lastname, 'Tester')
        self.assertEqual(toimari.position, 'Keppitiimi')
        self.assertEqual(toimari.section, self.test_jaosto2)

        self.assertRedirects(response, '/admin/')
