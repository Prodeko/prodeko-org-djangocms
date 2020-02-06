from django.test import override_settings

from .test_data import TestData

# Override settigs to test translations
english = override_settings(LANGUAGE_CODE="en", LANGUAGES=(("en", "English"),))

finnish = override_settings(LANGUAGE_CODE="fi", LANGUAGES=(("fi", "Finnish"),))


class JaostoModelTest(TestData):
    """Tests for Jaosto model."""

    @english
    def test_name_label_english(self):
        field_label = self.test_jaosto1._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "Name")

    @finnish
    def test_name_label_finnish(self):
        field_label = self.test_jaosto1._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "Nimi")

    def test_name_max_length(self):
        max_length = self.test_jaosto1._meta.get_field("name").max_length
        self.assertEquals(max_length, 50)


class ToimariModelTest(TestData):
    """Tests for Toimari model."""

    @english
    def test_firstname_label_english(self):
        field_label = self.test_toimari1._meta.get_field("firstname").verbose_name
        self.assertEquals(field_label, "First name")

    @finnish
    def test_firstname_label_finnish(self):
        field_label = self.test_toimari1._meta.get_field("firstname").verbose_name
        self.assertEquals(field_label, "Etunimi")

    def test_firstname_max_length(self):
        max_length = self.test_toimari1._meta.get_field("firstname").max_length
        self.assertEquals(max_length, 30)

    @english
    def test_lastname_label_english(self):
        field_label = self.test_toimari1._meta.get_field("lastname").verbose_name
        self.assertEquals(field_label, "Last name")

    @finnish
    def test_lastname_label_finnish(self):
        field_label = self.test_toimari1._meta.get_field("lastname").verbose_name
        self.assertEquals(field_label, "Sukunimi")

    def test_lastnamename_max_length(self):
        max_length = self.test_toimari1._meta.get_field("lastname").max_length
        self.assertEquals(max_length, 30)

    @english
    def test_position_label_english(self):
        field_label = self.test_toimari1._meta.get_field("position").verbose_name
        self.assertEquals(field_label, "Position")

    @finnish
    def test_position_label_finnish(self):
        field_label = self.test_toimari1._meta.get_field("position").verbose_name
        self.assertEquals(field_label, "Virka")

    def test_position_max_length(self):
        max_length = self.test_toimari1._meta.get_field("position").max_length
        self.assertEquals(max_length, 50)

    @english
    def test_section_label_english(self):
        field_label = self.test_toimari1._meta.get_field("section").verbose_name
        self.assertEquals(field_label, "Section")

    @finnish
    def test_section_label_finnish(self):
        field_label = self.test_toimari1._meta.get_field("section").verbose_name
        self.assertEquals(field_label, "Jaosto")


class HallituksenJasenModelTest(TestData):
    """Tests for HallituksenJasen model."""

    @english
    def test_firstname_label_english(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "firstname"
        ).verbose_name
        self.assertEquals(field_label, "First name")

    @finnish
    def test_firstname_label_finnish(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "firstname"
        ).verbose_name
        self.assertEquals(field_label, "Etunimi")

    def test_firstname_max_length(self):
        max_length = self.test_hallituksenjasen1._meta.get_field("firstname").max_length
        self.assertEquals(max_length, 30)

    @english
    def test_lastname_label_english(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "lastname"
        ).verbose_name
        self.assertEquals(field_label, "Last name")

    @finnish
    def test_lastname_label_finnish(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "lastname"
        ).verbose_name
        self.assertEquals(field_label, "Sukunimi")

    def test_lastnamename_max_length(self):
        max_length = self.test_hallituksenjasen1._meta.get_field("lastname").max_length
        self.assertEquals(max_length, 30)

    @english
    def test_position_label_english(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "position"
        ).verbose_name
        self.assertEquals(field_label, "Position")

    @finnish
    def test_position_label_finnish(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "position"
        ).verbose_name
        self.assertEquals(field_label, "Virka")

    def test_position_max_length(self):
        max_length = self.test_hallituksenjasen1._meta.get_field("position").max_length
        self.assertEquals(max_length, 50)

    @english
    def test_section_label_english(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "section"
        ).verbose_name
        self.assertEquals(field_label, "Section")

    @finnish
    def test_section_label_finnish(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "section"
        ).verbose_name
        self.assertEquals(field_label, "Jaosto")

    @english
    def test_position_en_label_english(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "position_en"
        ).verbose_name
        self.assertEquals(field_label, "Position (English)")

    @finnish
    def test_position_en_label_finnish(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "position_en"
        ).verbose_name
        self.assertEquals(field_label, "Virka (Englanniksi)")

    def test_position_en_max_length(self):
        max_length = self.test_hallituksenjasen1._meta.get_field(
            "position_en"
        ).max_length
        self.assertEquals(max_length, 60)

    @english
    def test_mobilephone_label_english(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "mobilephone"
        ).verbose_name
        self.assertEquals(field_label, "Mobile phone")

    @finnish
    def test_mobilephone_label_finnish(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "mobilephone"
        ).verbose_name
        self.assertEquals(field_label, "Puhelinnumero")

    def test_mobilephone_max_length(self):
        max_length = self.test_hallituksenjasen1._meta.get_field(
            "mobilephone"
        ).max_length
        self.assertEquals(max_length, 20)

    @english
    def test_email_label_english(self):
        field_label = self.test_hallituksenjasen1._meta.get_field("email").verbose_name
        self.assertEquals(field_label, "Email")

    @finnish
    def test_email_label_finnish(self):
        field_label = self.test_hallituksenjasen1._meta.get_field("email").verbose_name
        self.assertEquals(field_label, "Sähköposti")

    def test_email_max_length(self):
        max_length = self.test_hallituksenjasen1._meta.get_field("email").max_length
        self.assertEquals(max_length, 30)

    @english
    def test_telegram_label_english(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "telegram"
        ).verbose_name
        self.assertEquals(field_label, "Telegram")

    @finnish
    def test_telegram_label_finnish(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "telegram"
        ).verbose_name
        self.assertEquals(field_label, "Telegram")

    def test_telegram_max_length(self):
        max_length = self.test_hallituksenjasen1._meta.get_field("telegram").max_length
        self.assertEquals(max_length, 20)

    @english
    def test_description_label_english(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "description"
        ).verbose_name
        self.assertEquals(field_label, "Description")

    @finnish
    def test_description_label_finnish(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "description"
        ).verbose_name
        self.assertEquals(field_label, "Kuvaus")

    def test_description_max_length(self):
        max_length = self.test_hallituksenjasen1._meta.get_field(
            "description"
        ).max_length
        self.assertEquals(max_length, 255)
