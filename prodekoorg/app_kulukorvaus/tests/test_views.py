from .test_data import TestData
from django.urls import reverse


class KulukorvausViewTest(TestData):
    def test_download_and_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('app_kulukorvaus:download_kulukorvaus', kwargs={
                                   'perustiedot_id': self.test_perustiedot_model.id}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_kulukorvaus_and_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('app_kulukorvaus:kulukorvaus'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))

    def test_download_if_not_correct_permissions(self):
        self.client.login(email='test2@test.com', password='q"WaXkcB>7')
        response = self.client.get(reverse('app_kulukorvaus:download_kulukorvaus', kwargs={
                                   'perustiedot_id': self.test_perustiedot_model.id}))
        self.assertEqual(response.status_code, 403)

    def test_download_correct_permissions(self):
        self.client.login(email='test1@test.com', password='Ukc55Has-@')
        response = self.client.get(reverse('app_kulukorvaus:download_kulukorvaus', kwargs={
                                   'perustiedot_id': self.test_perustiedot_model.id}))
        self.assertEqual(response.status_code, 200)

    def test_HTTP404_for_invalid_reimbursement_if_logged_in(self):
        self.client.login(email='test1@test.com', password='Ukc55Has-@')
        response = self.client.get(reverse('app_kulukorvaus:download_kulukorvaus', kwargs={
                                   'perustiedot_id': 999}))
        self.assertEqual(response.status_code, 404)

    def test_form_submission(self):
        self.client.login(email='test1@test.com', password='Ukc55Has-@')
        data = {
            # management_form data
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',

            # First Kulukorvaus data
            'form-0-sum_euros': '23',
            'form-0-info': None,
            'form-0-explanation': 'Testing',
            'form-0-additional_info': '',
            'form-0-target': 'Test',
            'form-0-receipt': self.file_mock_jpg,

            # Second kulukorvaus data
            'form-1-sum_euros': '9001',
            'form-1-info': None,
            'form-1-explanation': 'Testing',
            'form-1-additional_info': '',
            'form-1-target': 'Test2',
            'form-1-receipt': self.file_mock_jpg
        }

        response = self.client.post(reverse("app_kulukorvaus:kulukorvaus"), data)
        self.assertEqual(response.status_code, 200)
