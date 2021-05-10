import os

import lxml
import pytest
from bs4 import BeautifulSoup
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.utils import override_settings

from .test_data import TestData

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
test_img1 = open(os.path.join(__location__, "img1.jpg"), "rb")
test_img2 = open(os.path.join(__location__, "img2.jpg"), "rb")


class KulukorvausViewTest(TestData):
    """Tests for views in the app_kulukorvaus app."""

    def test_kulukorvaus_and_redirect_not_logged_in(self):
        """
        Tests redirect to login page if the main kulukorvaus page is
        accessed and the user is not logged in.
        """

        response = self.client.get("/fi/kulukorvaus/")
        self.assertRedirects(response, "/fi/login/?next=/fi/kulukorvaus/")

    def test_download_and_redirect_not_logged_in(self):
        """
        Tests redirect to login page if the download url is accessed
        and the user is not logged in.
        """

        response = self.client.get(
            f"/fi/kulukorvaus/download/{self.test_perustiedot_model.id}"
        )
        self.assertRedirects(
            response,
            f"/fi/login/?next=/fi/kulukorvaus/download/{self.test_perustiedot_model.id}",
        )

    def test_download_incorrect_permissions(self):
        """
        Test that a user who didn't create the kulukorvaus can't download it.
        """

        self.client.login(email="test2@test.com", password="test2salasana")
        response = self.client.get(
            f"/fi/kulukorvaus/download/{self.test_perustiedot_model.id}"
        )
        self.assertEqual(response.status_code, 403)

    def test_download_correct_permissions(self):
        """
        Tests that a user who created the kulukorvaus can download it.
        """

        self.client.login(email="test1@test.com", password="test1salasana")
        response = self.client.get(
            f"/fi/kulukorvaus/download/{self.test_perustiedot_model.id}"
        )
        self.assertEqual(
            response.get("Content-Disposition"),
            'attachment; filename="' + self.test_perustiedot_model.pdf_filename() + '"',
        )

    def test_prepopulate_form(self):
        """
        Tests that prepopulating the form fields work.
        """

        self.client.login(email="test1@test.com", password="test1salasana")
        response = self.client.get(f"/fi/kulukorvaus/")

        soup = BeautifulSoup(response.content, "lxml")
        input_created_by = soup.find("input", {"id": "id_created_by"})
        input_email = soup.find("input", {"id": "id_email"})

        self.assertHTMLEqual(
            str(input_created_by),
            '<input class="form-control" id="id_created_by" maxlength="50" name="created_by" required="" type="text" value="Testi 1"/>',
        )
        self.assertHTMLEqual(
            str(input_email),
            '<input class="form-control" id="id_email" maxlength="254" name="email" required="" type="email" value="test1@test.com"/>',
        )

    def test_invalid_reimbursement_logged_in(self):
        """
        Tests that HTTP404 is raised if someone tries to download
        a non-existent kulukorvaus.
        """

        self.client.login(email="test1@test.com", password="test1salasana")
        response = self.client.get("/fi/kulukorvaus/download/999")
        self.assertEqual(response.status_code, 404)

    @pytest.mark.skipif(
        os.getenv("CI", "false") == "true",
        reason="TODO: figure out why this test does not work in CI. Might have something to do with sample variables being used in CI.",
    )
    def test_form_submission(self):
        """
        Test valid form submission. Includes the empty/management form data.
        """

        self.client.login(email="test1@test.com", password="test1salasana")

        test_data = {
            # management_form data
            "form-TOTAL_FORMS": "2",
            "form-INITIAL_FORMS": "0",
            "form-MIN_NUM_FORMS": "0",
            "form-MAX_NUM_FORMS": "1000",
            # KulukorvausPerustiedotForm
            "created_by": "Mediakeisari Timo Riski",
            "email": "webbitiimi@prodeko.org",
            "phone_number": "123456789",
            "bank_number": "FI21 1234 5600 0007 85",
            "bic": "Nordea",
            "sum_overall": "1.51",
            "additional_info": "Tämä on testi!",
            # First KulukorvausForm data
            "form-0-sum_euros": "23",
            "form-0-explanation": "Testing",
            "form-0-additional_info": "",
            "form-0-target": "Test",
            "form-0-receipt": SimpleUploadedFile("test.jpg", test_img1.read()),
            # Second KulukorvausForm data
            "form-1-sum_euros": "9001",
            "form-1-explanation": "Testing",
            "form-1-additional_info": "",
            "form-1-target": "Test2",
            "form-1-receipt": SimpleUploadedFile("test2.jpg", test_img2.read()),
        }

        response = self.client.post(
            "/fi/kulukorvaus/",
            data=test_data,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 2)
        self.assertContains(
            response,
            "✅ Kulukorvauksesi on vastaanotettu.",
        )

    def test_form_submission_has_not_accepted_policies(self):
        """
        Test form submission if the user hasn't accepted policies.
        """

        self.client.login(email="test2@test.com", password="test2salasana")

        test_data = {
            # management_form data
            "form-TOTAL_FORMS": "2",
            "form-INITIAL_FORMS": "0",
            "form-MIN_NUM_FORMS": "0",
            "form-MAX_NUM_FORMS": "1000",
            # KulukorvausPerustiedotForm
            "created_by": "Prodekon CTO",
            "email": "webbitiimi@prodeko.org",
            "phone_number": "123456789",
            "bank_number": "FI21 1234 5600 0007 85",
            "bic": "Nordea",
            "sum_overall": "200",
            "additional_info": "Tämä on testi!",
            # First KulukorvausForm data
            "form-0-sum_euros": "200",
            "form-0-explanation": "Webbitiimin virkistys",
            "form-0-additional_info": "",
            "form-0-target": "Webbitiimi",
            "form-0-receipt": SimpleUploadedFile("test.jpg", test_img1.read()),
        }

        response = self.client.post(
            "/fi/kulukorvaus/",
            data=test_data,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.context["policy_error"], True)
        self.assertContains(
            response,
            "Käyttääksesi Prodekon sähköisiä palveluita, sinun on hyväksyttävä",
        )

    def test_invalid_form_submission(self):
        """
        Test invalid form submission. The email is invalid.
        """

        self.client.login(email="test1@test.com", password="test1salasana")

        test_data = {
            # management_form data
            "form-TOTAL_FORMS": "2",
            "form-INITIAL_FORMS": "0",
            "form-MIN_NUM_FORMS": "0",
            "form-MAX_NUM_FORMS": "1000",
            # KulukorvausPerustiedotForm
            "created_by": "Mediakeisari Timo Riski",
            "email": "webbitiimi",  # This is incorrect
            "phone_number": "123456789",
            "bank_number": "FI21 1234 5600 0007 85",
            "bic": "Nordea",
            "sum_overall": "1.51",
            "additional_info": "Tämä on testi!",
            # First KulukorvausForm data
            "form-0-sum_euros": "23",
            "form-0-explanation": "Testing",
            "form-0-additional_info": "",
            "form-0-target": "Test",
            "form-0-receipt": SimpleUploadedFile("test.jpg", test_img1.read()),
            # Second KulukorvausForm data
            "form-1-sum_euros": "9001",
            "form-1-explanation": "Testing",
            "form-1-additional_info": "",
            "form-1-target": "Test2",
            "form-1-receipt": SimpleUploadedFile("test2.jpg", test_img2.read()),
        }

        response = self.client.post(
            "/fi/kulukorvaus/",
            data=test_data,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertContains(
            response, "Syötä kelvollinen sähköpostiosoite", status_code=599
        )
