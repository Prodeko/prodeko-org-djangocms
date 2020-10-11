from prodekoorg.app_utils.tests.test_utils import english, finnish

from .test_data import TestData


class PendingUserModelTest(TestData):
    """Tests for PendingUser model."""

    @english
    def test_first_name_label_english(self):
        field_label = self.test_pendinguser_model._meta.get_field(
            "first_name"
        ).verbose_name
        self.assertEqual(field_label, "First name")

    @finnish
    def test_first_name_label_finnish(self):
        field_label = self.test_pendinguser_model._meta.get_field(
            "first_name"
        ).verbose_name
        self.assertEqual(field_label, "Etunimi")

    def test_first_name_max_length(self):
        max_length = self.test_pendinguser_model._meta.get_field(
            "first_name"
        ).max_length
        self.assertEqual(max_length, 50)

    @english
    def test_last_name_label_english(self):
        field_label = self.test_pendinguser_model._meta.get_field(
            "last_name"
        ).verbose_name
        self.assertEqual(field_label, "Last name")

    @finnish
    def test_last_name_label_finnish(self):
        field_label = self.test_pendinguser_model._meta.get_field(
            "last_name"
        ).verbose_name
        self.assertEqual(field_label, "Sukunimi")

    def test_last_name_max_length(self):
        max_length = self.test_pendinguser_model._meta.get_field("last_name").max_length
        self.assertEqual(max_length, 50)

    @english
    def test_hometown_label_english(self):
        field_label = self.test_pendinguser_model._meta.get_field(
            "hometown"
        ).verbose_name
        self.assertEqual(field_label, "Hometown")

    @finnish
    def test_hometown_label_finnish(self):
        field_label = self.test_pendinguser_model._meta.get_field(
            "hometown"
        ).verbose_name
        self.assertEqual(field_label, "Kotikaupunki")

    def test_hometown_max_length(self):
        max_length = self.test_pendinguser_model._meta.get_field("hometown").max_length
        self.assertEqual(max_length, 50)

    @english
    def test_field_of_study_label_english(self):
        field_label = self.test_pendinguser_model._meta.get_field(
            "field_of_study"
        ).verbose_name
        self.assertEqual(field_label, "Field of study")

    @finnish
    def test_field_of_study_label_finnish(self):
        field_label = self.test_pendinguser_model._meta.get_field(
            "field_of_study"
        ).verbose_name
        self.assertEqual(field_label, "Opiskeluala")

    def test_field_of_study_max_length(self):
        max_length = self.test_pendinguser_model._meta.get_field(
            "field_of_study"
        ).max_length
        self.assertEqual(max_length, 50)

    @english
    def test_email_label_english(self):
        field_label = self.test_pendinguser_model._meta.get_field("email").verbose_name
        self.assertEqual(field_label, "Email")

    @finnish
    def test_email_label_finnish(self):
        field_label = self.test_pendinguser_model._meta.get_field("email").verbose_name
        self.assertEqual(field_label, "Sähköposti")

    @english
    def test_start_year_label_english(self):
        field_label = self.test_pendinguser_model._meta.get_field(
            "start_year"
        ).verbose_name
        self.assertEqual(field_label, "Start year of studies")

    @finnish
    def test_start_year_label_finnish(self):
        field_label = self.test_pendinguser_model._meta.get_field(
            "start_year"
        ).verbose_name
        self.assertEqual(field_label, "Aloitusvuosi")

    @english
    def test_language_label_english(self):
        field_label = self.test_pendinguser_model._meta.get_field(
            "language"
        ).verbose_name
        self.assertEqual(field_label, "Preferred language")

    @finnish
    def test_language_label_finnish(self):
        field_label = self.test_pendinguser_model._meta.get_field(
            "language"
        ).verbose_name
        self.assertEqual(field_label, "Kieli")

    @english
    def test_membership_type_label_english(self):
        field_label = self.test_pendinguser_model._meta.get_field(
            "membership_type"
        ).verbose_name
        self.assertEqual(field_label, "Membership type")

    @finnish
    def test_membership_type_label_finnish(self):
        field_label = self.test_pendinguser_model._meta.get_field(
            "membership_type"
        ).verbose_name
        self.assertEqual(field_label, "Jäsentyyppi")

    @english
    def test_additional_info_label_english(self):
        field_label = self.test_pendinguser_model._meta.get_field(
            "additional_info"
        ).verbose_name
        self.assertEqual(field_label, "Why do you want to become a member?")

    @finnish
    def test_additional_info_label_finnish(self):
        field_label = self.test_pendinguser_model._meta.get_field(
            "additional_info"
        ).verbose_name
        self.assertEqual(field_label, "Miksi haluat jäseneksi?")

    @english
    def test_is_ayy_member_label_english(self):
        field_label = self.test_pendinguser_model._meta.get_field(
            "is_ayy_member"
        ).verbose_name
        self.assertEqual(
            field_label, "Are you an AYY (Aalto University Student Union) member?"
        )

    @finnish
    def test_is_ayy_member_label_finnish(self):
        field_label = self.test_pendinguser_model._meta.get_field(
            "is_ayy_member"
        ).verbose_name
        self.assertEqual(field_label, "Oletko AYY:n jäsen?")

    @english
    def test_receipt_label_english(self):
        field_label = self.test_pendinguser_model._meta.get_field(
            "receipt"
        ).verbose_name
        self.assertEqual(field_label, "Receipt of the membership payment")

    @finnish
    def test_receipt_label_finnish(self):
        field_label = self.test_pendinguser_model._meta.get_field(
            "receipt"
        ).verbose_name
        self.assertEqual(field_label, "Kuitti jäsenmaksusta")

    @english
    def test_has_accepted_policies_label_english(self):
        field_label = self.test_pendinguser_model._meta.get_field(
            "has_accepted_policies"
        ).verbose_name
        self.assertEqual(field_label, "I accept Prodeko's privacy policy")

    @finnish
    def test_has_accepted_policies_label_finnish(self):
        field_label = self.test_pendinguser_model._meta.get_field(
            "has_accepted_policies"
        ).verbose_name
        self.assertEqual(field_label, "Hyväksyn Prodekon tietosuojalausekkeen")
