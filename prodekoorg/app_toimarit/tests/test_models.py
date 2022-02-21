from prodekoorg.app_utils.tests.test_utils import english, finnish

from .test_data import TestData


class JaostoModelTest(TestData):
    """Tests for Jaosto model."""

    @english
    def test_name_label_english(self):
        field_label = self.test_jaosto1._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "Name")

    @finnish
    def test_name_label_finnish(self):
        field_label = self.test_jaosto1._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "Nimi")

    def test_name_max_length(self):
        max_length = self.test_jaosto1._meta.get_field("name").max_length
        self.assertEqual(max_length, 50)


class ToimariModelTest(TestData):
    """Tests for Toimari model."""

    @english
    def test_firstname_label_english(self):
        field_label = self.test_toimari1._meta.get_field("firstname").verbose_name
        self.assertEqual(field_label, "First name")

    @finnish
    def test_firstname_label_finnish(self):
        field_label = self.test_toimari1._meta.get_field("firstname").verbose_name
        self.assertEqual(field_label, "Etunimi")

    def test_firstname_max_length(self):
        max_length = self.test_toimari1._meta.get_field("firstname").max_length
        self.assertEqual(max_length, 30)

    @english
    def test_lastname_label_english(self):
        field_label = self.test_toimari1._meta.get_field("lastname").verbose_name
        self.assertEqual(field_label, "Last name")

    @finnish
    def test_lastname_label_finnish(self):
        field_label = self.test_toimari1._meta.get_field("lastname").verbose_name
        self.assertEqual(field_label, "Sukunimi")

    def test_lastnamename_max_length(self):
        max_length = self.test_toimari1._meta.get_field("lastname").max_length
        self.assertEqual(max_length, 30)

    @english
    def test_position_label_english(self):
        field_label = self.test_toimari1._meta.get_field("position").verbose_name
        self.assertEqual(field_label, "Position")

    @finnish
    def test_position_label_finnish(self):
        field_label = self.test_toimari1._meta.get_field("position").verbose_name
        self.assertEqual(field_label, "Virka")

    def test_position_max_length(self):
        max_length = self.test_toimari1._meta.get_field("position").max_length
        self.assertEqual(max_length, 50)

    @english
    def test_section_label_english(self):
        field_label = self.test_toimari1._meta.get_field("section").verbose_name
        self.assertEqual(field_label, "Section")

    @finnish
    def test_section_label_finnish(self):
        field_label = self.test_toimari1._meta.get_field("section").verbose_name
        self.assertEqual(field_label, "Jaosto")

    @english
    def test_photo_label_english(self):
        field_label = self.test_toimari1._meta.get_field("photo").verbose_name
        self.assertEqual(field_label, "Photo")

    @finnish
    def test_photo_label_finnish(self):
        field_label = self.test_toimari1._meta.get_field("photo").verbose_name
        self.assertEqual(field_label, "Kuva")

    @english
    def test_year_label_english(self):
        field_label = self.test_toimari1._meta.get_field("year").verbose_name
        self.assertEqual(field_label, "Year")

    @finnish
    def test_year_label_finnish(self):
        field_label = self.test_toimari1._meta.get_field("year").verbose_name
        self.assertEqual(field_label, "Vuosi")


class HallituksenJasenModelTest(TestData):
    """Tests for HallituksenJasen model."""

    @english
    def test_firstname_label_english(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "firstname"
        ).verbose_name
        self.assertEqual(field_label, "First name")

    @finnish
    def test_firstname_label_finnish(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "firstname"
        ).verbose_name
        self.assertEqual(field_label, "Etunimi")

    def test_firstname_max_length(self):
        max_length = self.test_hallituksenjasen1._meta.get_field("firstname").max_length
        self.assertEqual(max_length, 30)

    @english
    def test_lastname_label_english(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "lastname"
        ).verbose_name
        self.assertEqual(field_label, "Last name")

    @finnish
    def test_lastname_label_finnish(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "lastname"
        ).verbose_name
        self.assertEqual(field_label, "Sukunimi")

    def test_lastname_max_length(self):
        max_length = self.test_hallituksenjasen1._meta.get_field("lastname").max_length
        self.assertEqual(max_length, 30)

    @english
    def test_position_fi_label_english(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "position_fi"
        ).verbose_name
        self.assertEqual(field_label, "Position")

    @finnish
    def test_position_fi_label_finnish(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "position_fi"
        ).verbose_name
        self.assertEqual(field_label, "Virka")

    def test_position_fi_max_length(self):
        max_length = self.test_hallituksenjasen1._meta.get_field(
            "position_fi"
        ).max_length
        self.assertEqual(max_length, 50)

    @english
    def test_position_en_label_english(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "position_en"
        ).verbose_name
        self.assertEqual(field_label, "Position (English)")

    def test_position_en_max_length(self):
        max_length = self.test_hallituksenjasen1._meta.get_field(
            "position_en"
        ).max_length
        self.assertEqual(max_length, 60)

    @finnish
    def test_position_en_label_finnish(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "position_en"
        ).verbose_name
        self.assertEqual(field_label, "Virka (Englanniksi)")

    def test_position_en_max_length_two(self):
        max_length = self.test_hallituksenjasen1._meta.get_field(
            "position_en"
        ).max_length
        self.assertEqual(max_length, 60)

    @english
    def test_mobilephone_label_english(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "mobilephone"
        ).verbose_name
        self.assertEqual(field_label, "Mobile phone")

    @finnish
    def test_mobilephone_label_finnish(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "mobilephone"
        ).verbose_name
        self.assertEqual(field_label, "Puhelinnumero")

    def test_mobilephone_max_length(self):
        max_length = self.test_hallituksenjasen1._meta.get_field(
            "mobilephone"
        ).max_length
        self.assertEqual(max_length, 20)

    @english
    def test_email_label_english(self):
        field_label = self.test_hallituksenjasen1._meta.get_field("email").verbose_name
        self.assertEqual(field_label, "Email")

    @finnish
    def test_email_label_finnish(self):
        field_label = self.test_hallituksenjasen1._meta.get_field("email").verbose_name
        self.assertEqual(field_label, "Sähköposti")

    def test_email_max_length(self):
        max_length = self.test_hallituksenjasen1._meta.get_field("email").max_length
        self.assertEqual(max_length, 30)

    @english
    def test_telegram_label_english(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "telegram"
        ).verbose_name
        self.assertEqual(field_label, "Telegram")

    @finnish
    def test_telegram_label_finnish(self):
        field_label = self.test_hallituksenjasen1._meta.get_field(
            "telegram"
        ).verbose_name
        self.assertEqual(field_label, "Telegram")

    def test_telegram_max_length(self):
        max_length = self.test_hallituksenjasen1._meta.get_field("telegram").max_length
        self.assertEqual(max_length, 20)

    @english
    def test_photo_label_english(self):
        field_label = self.test_hallituksenjasen1._meta.get_field("photo").verbose_name
        self.assertEqual(field_label, "Photo")

    @finnish
    def test_photo_label_finnish(self):
        field_label = self.test_hallituksenjasen1._meta.get_field("photo").verbose_name
        self.assertEqual(field_label, "Kuva")

    @english
    def test_year_label_english(self):
        field_label = self.test_hallituksenjasen1._meta.get_field("year").verbose_name
        self.assertEqual(field_label, "Year")

    @finnish
    def test_year_label_finnish(self):
        field_label = self.test_hallituksenjasen1._meta.get_field("year").verbose_name
        self.assertEqual(field_label, "Vuosi")
