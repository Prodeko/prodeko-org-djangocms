import os
from unittest.mock import Mock, patch

import pytest
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.utils import override_settings

from .test_data import TestData


class MembershipViewTest(TestData):
    """Tests for views in the app_membership app."""

    @patch("prodekoorg.app_membership.groups_api.initialize_service")
    def test_accept_membership(self, mock_initialize_service):
        """
        Tests accepting a membership application from the admin panel.
        """

        mock_initialize_service.members.insert.execute = Mock()

        self.client.login(email="test2@test.com", password="test2salasana")

        response = self.client.get(
            f"/fi/admin/app_membership/pendinguser/{self.test_pendinguser_model.id}/accept/",
            follow=True,
        )

        self.assertContains(
            response, "Jäsenhakemus hyväksytty",
        )
        self.assertContains(
            response,
            f"Lisätty {self.test_pendinguser_model.email} onnistuneesti test@prodeko.org sähköpostilistalle.",
        )
        self.assertContains(
            response,
            f"Lisätty {self.test_pendinguser_model.email} onnistuneesti test@raittiusseura.org sähköpostilistalle.",
        )

        self.assertRedirects(
            response, f"/fi/admin/app_membership/pendinguser/",
        )
        self.assertEqual(len(mail.outbox), 1)
        subject = "Hakemuksesi Prodekon jäseneksi hyväksyttiin"
        self.assertEqual(mail.outbox[0].subject, subject)

    @patch("prodekoorg.app_membership.groups_api.initialize_service")
    def test_reject_membership(self, mock_initialize_service):
        """
        Tests rejecting a membership application from the admin panel.
        """

        mock_initialize_service.members.insert.execute = Mock()

        self.client.login(email="test2@test.com", password="test2salasana")

        applicant = self.test_pendinguser_model

        response = self.client.get(
            f"/fi/admin/app_membership/pendinguser/{applicant.id}/reject/", follow=True,
        )

        self.assertContains(
            response, "Jäsenhakemus hylätty",
        )

        self.assertRedirects(
            response, f"/fi/admin/app_membership/pendinguser/",
        )
        self.assertEqual(len(mail.outbox), 1)
        subject = "Hakemuksesi Prodekon jäseneksi hylättiin"
        self.assertEqual(mail.outbox[0].subject, subject)

    def test_form_submission(self):
        """
        Test valid form submission. Includes the empty/management form data.
        """

        self.client.login(email="test1@test.com", password="test1salasana")

        test_data = {
            "id": 1,
            "first_name": "Prodekon",
            "last_name": "Mediakeisari",
            "hometown": "Espoo",
            "field_of_study": "Tuotantotalous",
            "email": "test3@ptest.org",
            "start_year": 2017,
            "language": "FI",
            "membership_type": "TR",
            "additional_info": "muistakaa tehdä testejä!",
            "is_ayy_member": "Y",
            "receipt": SimpleUploadedFile("test.jpg", b"a"),
            "has_accepted_policies": True,
        }

        response = self.client.post(
            "/fi/jasenhakemus/", data=test_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "📬 Hakemus vastaanotettu!",
        )
        self.assertEqual(len(mail.outbox), 1)
        subject = "Uusi jäsenhakemus - Prodekon Mediakeisari"
        self.assertEqual(mail.outbox[0].subject, subject)

    def test_invalid_form_submission(self):
        """
        Test invalid form submission. The email is invalid.
        """

        self.client.login(email="test1@test.com", password="test1salasana")

        test_data = {
            "id": 1,
            "first_name": "Mediakeisari",
            "last_name": "Mediakeisari",
            "hometown": "Espoo",
            "field_of_study": "Tuotantotalous",
            "email": "test3",
            "start_year": 2017,
            "language": "FI",
            "membership_type": "TR",
            "additional_info": "muistakaa tehdä testejä!",
            "is_ayy_member": "Y",
            "receipt": SimpleUploadedFile("test.jpg", b"a"),
            "has_accepted_policies": True,
        }

        response = self.client.post(
            "/fi/jasenhakemus/", data=test_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertContains(
            response, "Syötä kelvollinen sähköpostiosoite", status_code=599
        )
