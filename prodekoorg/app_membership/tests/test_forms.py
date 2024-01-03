from django.core.files.uploadedfile import SimpleUploadedFile

from ..forms import PendingUserForm
from .test_data import TestData


class PendingUserFormFormTest(TestData):
    """Tests for PendingUserForm."""

    def test_pending_user_form_valid(self):
        form_data = {
            "id": 1,
            "first_name": "Test",
            "last_name": "1",
            "hometown": "Espoo",
            "field_of_study": "Tuotantotalous",
            "email": "test1@test.co",
            "start_year": 2017,
            "language": "FI",
            "membership_type": "TR",
            "additional_info": "muistakaa tehdä testejä!",
            "is_ayy_member": "Y",
            "has_accepted_policies": True,
        }
        file_data = {"receipt": SimpleUploadedFile("test.jpg", b"a")}
        form = PendingUserForm(data=form_data, files=file_data)

        self.assertTrue(form.is_valid())

    def test_pending_user_form_invalid_multiple(self):
        form_data = {
            "id": 1,
            "first_name": "Mediakeisari",
            "last_name": "Mediakeisari",
            "hometown": "Espoo",
            "field_of_study": "Tuotantotalous",
            "email": "webbitiimi@prodeko.org",
            "start_year": 2030,
            "language": "XD",
            "membership_type": "DD",
            "additional_info": "muistakaa tehdä testejä!",
            "is_ayy_member": "A",
            "has_accepted_policies": True,
        }
        form = PendingUserForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)
        self.assertTrue(form["start_year"].errors)
        self.assertTrue(form["language"].errors)
        self.assertTrue(form["membership_type"].errors)
        self.assertTrue(form["is_ayy_member"].errors)
        self.assertTrue(form["email"].errors)
