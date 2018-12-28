import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .test_data import TestData


class KulukorvausViewTest(TestData):
    """Tests for views in the app_kulukorvaus app."""

    def test_kulukorvaus_and_redirect_if_not_logged_in(self):
        """
        Tests redirect to login page if the main kulukorvaus page is
        accessed and the user is not logged in.
        """
        response = self.client.get(reverse('app_kulukorvaus:kulukorvaus'))
        self.assertRedirects(response, '/login/?next=/kulukorvaus/')

    def test_download_and_redirect_if_not_logged_in(self):
        """
        Tests redirect to login page if the download url is accessed
        and the user is not logged in.
        """
        response = self.client.get(reverse('app_kulukorvaus:download_kulukorvaus', kwargs={
                                   'perustiedot_id': self.test_perustiedot_model.id}))
        self.assertRedirects(response, '/login/?next=/download-kulukorvaus/1')

    def test_download_if_not_correct_permissions(self):
        """
        Test that a user who didn't create the kulukorvaus can't download it.
        """
        self.client.login(email='test2@test.com', password='q"WaXkcB>7')
        response = self.client.get(reverse('app_kulukorvaus:download_kulukorvaus', kwargs={
                                   'perustiedot_id': self.test_perustiedot_model.id}))
        self.assertEqual(response.status_code, 403)

    def test_download_correct_permissions(self):
        """
        Tests that a user who created the kulukorvaus can download it.
        """
        self.client.login(email='test1@test.com', password='Ukc55Has-@')
        response = self.client.get(reverse('app_kulukorvaus:download_kulukorvaus', kwargs={
                                   'perustiedot_id': self.test_perustiedot_model.id}))
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_reimbursement_if_logged_in(self):
        """
        Tests that HTTP404 is raised if someone tries to download
        a non-existent kulukorvaus.
        """
        self.client.login(email='test1@test.com', password='Ukc55Has-@')
        response = self.client.get(reverse('app_kulukorvaus:download_kulukorvaus', kwargs={
                                   'perustiedot_id': 999}))
        self.assertEqual(response.status_code, 404)

    def test_form_submission(self):
        """
        Test valid form submission. Includes the empty/management form data.
        """
        self.client.login(email='test1@test.com', password='Ukc55Has-@')

        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        test_img1 = open(os.path.join(__location__, 'img1.jpg'), "rb")
        test_img2 = open(os.path.join(__location__, 'img2.jpg'), "rb")

        test_data = {
            # management_form data
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',

            # KulukorvausPerustiedotForm
            'created_by': 'Mediakeisari Timo Riski',
            'email': 'webbitiimi@prodeko.org',
            'position_in_guild': 'H',
            'phone_number': '123456789',
            'bank_number': 'FI21 1234 5600 0007 85',
            'bic': 'NORDEA',
            'sum_overall': '1.51',
            'additional_info': 'Tämä on testi!',

            # First KulukorvausForm data
            'form-0-sum_euros': '23',
            'form-0-explanation': 'Testing',
            'form-0-additional_info': '',
            'form-0-target': 'Test',
            'form-0-receipt': SimpleUploadedFile('test.jpg', test_img1.read()),

            # Second KulukorvausForm data
            'form-1-sum_euros': '9001',
            'form-1-explanation': 'Testing',
            'form-1-additional_info': '',
            'form-1-target': 'Test2',
            'form-1-receipt': SimpleUploadedFile('test2.jpg', test_img2.read()),
        }

        response = self.client.post(reverse("app_kulukorvaus:kulukorvaus"), data=test_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_invalid_form_submission(self):
        """
        Test invalid form submission. The position_in_guild is invalid.
        """
        self.client.login(email='test1@test.com', password='Ukc55Has-@')

        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        test_img1 = open(os.path.join(__location__, 'img1.jpg'), "rb")
        test_img2 = open(os.path.join(__location__, 'img2.jpg'), "rb")

        test_data = {
            # management_form data
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',

            # KulukorvausPerustiedotForm
            'created_by': 'Mediakeisari Timo Riski',
            'email': 'webbitiimi@prodeko.org',
            'position_in_guild': 'A',  # This is incorrect
            'phone_number': '123456789',
            'bank_number': 'FI21 1234 5600 0007 85',
            'bic': 'NORDEA',
            'sum_overall': '1.51',
            'additional_info': 'Tämä on testi!',

            # First KulukorvausForm data
            'form-0-sum_euros': '23',
            'form-0-explanation': 'Testing',
            'form-0-additional_info': '',
            'form-0-target': 'Test',
            'form-0-receipt': SimpleUploadedFile('test.jpg', test_img1.read()),

            # Second KulukorvausForm data
            'form-1-sum_euros': '9001',
            'form-1-explanation': 'Testing',
            'form-1-additional_info': '',
            'form-1-target': 'Test2',
            'form-1-receipt': SimpleUploadedFile('test2.jpg', test_img2.read()),
        }

        response = self.client.post(reverse("app_kulukorvaus:kulukorvaus"), data=test_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 599)
