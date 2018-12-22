from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings

from ..models import KulukorvausPerustiedot, Kulukorvaus


# Override settigs to test translations
english = override_settings(
    LANGUAGE_CODE='en',
    LANGUAGES=(('en', 'English'),),
)

finnish = override_settings(
    LANGUAGE_CODE='fi',
    LANGUAGES=(('fi', 'Finnish'),),
)


class TestData(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        User = get_user_model()
        test_user1 = User.objects.create_user(
            email='test1@test.com', password='A9}tK&@v~v')

        perustiedot = KulukorvausPerustiedot.objects.create(created_by_user=test_user1,
                                                            created_by='webbitiimi',
                                                            email='webbitiimi@prodeko.org',
                                                            position_in_guild='T',
                                                            phone_number='999888777666',
                                                            bank_number='FI239482340924092',
                                                            bic='SPANKKI',
                                                            sum_overall=1234,
                                                            additional_info='Some additional info.',
                                                            pdf=b'',)

        Kulukorvaus.objects.create(info=perustiedot,
                                   target='Testing',
                                   explanation='Making sure that everything works as expected!',
                                   sum_euros=99.991,
                                   additional_info='Some additional info.',
                                   receipt=b'',)


class KulukorvausPerustiedotModelTest(TestData):
    @english
    def test_created_by_label_english(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        field_label = model._meta.get_field('created_by').verbose_name
        self.assertEquals(field_label, 'Name')

    @finnish
    def test_created_by_label_finnish(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        field_label = model._meta.get_field('created_by').verbose_name
        self.assertEquals(field_label, 'Nimi')

    def test_created_by_max_length(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        max_length = model._meta.get_field('created_by').max_length
        self.assertEquals(max_length, 50)

    @english
    def test_email_label_english(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        field_label = model._meta.get_field('email').verbose_name
        self.assertEquals(field_label, 'Email')

    @finnish
    def test_email_label_finnish(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        field_label = model._meta.get_field('email').verbose_name
        self.assertEquals(field_label, 'Sähköposti')

    @english
    def test_position_in_guild_label_english(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        field_label = model._meta.get_field('position_in_guild').verbose_name
        self.assertEquals(field_label, 'Position in guild')

    @finnish
    def test_position_in_guild_label_finnish(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        field_label = model._meta.get_field('position_in_guild').verbose_name
        self.assertEquals(field_label, 'Virka')

    def test_position_in_guild_max_length(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        max_length = model._meta.get_field('position_in_guild').max_length
        self.assertEquals(max_length, 12)

    @english
    def test_phone_number_label_english(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        field_label = model._meta.get_field('phone_number').verbose_name
        self.assertEquals(field_label, 'Phone number')

    @finnish
    def test_phone_number_label_finnish(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        field_label = model._meta.get_field('phone_number').verbose_name
        self.assertEquals(field_label, 'Puhelinnumero')

    def test_phone_number_max_length(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        max_length = model._meta.get_field('phone_number').max_length
        self.assertEquals(max_length, 15)

    @english
    def test_bank_number_label_english(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        field_label = model._meta.get_field('bank_number').verbose_name
        self.assertEquals(field_label, 'Account number (IBAN)')

    @finnish
    def test_bank_number_label_finnish(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        field_label = model._meta.get_field('bank_number').verbose_name
        self.assertEquals(field_label, 'Tilinumero (IBAN)')

    def test_bank_number_max_length(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        max_length = model._meta.get_field('bank_number').max_length
        self.assertEquals(max_length, 32)

    def test_bic_label(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        field_label = model._meta.get_field('bic').verbose_name
        self.assertEquals(field_label, 'BIC')

    def test_bic_max_length(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        max_length = model._meta.get_field('bic').max_length
        self.assertEquals(max_length, 11)

    @english
    def test_sum_overall_label_english(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        field_label = model._meta.get_field('sum_overall').verbose_name
        self.assertEquals(field_label, 'Total reimbursement (in €)')

    @finnish
    def test_sum_overall_label_finnish(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        field_label = model._meta.get_field('sum_overall').verbose_name
        self.assertEquals(field_label, 'Korvaussumma yhteensä (euroissa)')

    def test_sum_overall_max_digits(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        max_digits = model._meta.get_field('sum_overall').max_digits
        decimal_places = model._meta.get_field('sum_overall').decimal_places
        self.assertEquals(max_digits, 10)
        self.assertEquals(decimal_places, 2)

    @english
    def test_additional_info_label_english(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        field_label = model._meta.get_field('additional_info').verbose_name
        self.assertEquals(field_label, 'Additional information')

    @finnish
    def test_additional_info_label_finnish(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        field_label = model._meta.get_field('additional_info').verbose_name
        self.assertEquals(field_label, 'Lisätietoja, kulujen perusteita')

    def test_pdf_label(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        field_label = model._meta.get_field('pdf').verbose_name
        self.assertEquals(field_label, 'PDF')

    @english
    def test_object_name_english(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        expected_object_name = '{}, {}€'.format(
            model.created_by, model.sum_overall)
        self.assertEquals(expected_object_name, str(model))

    @finnish
    def test_object_name_finnish(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        expected_object_name = '{}, {}€'.format(
            model.created_by, model.sum_overall)
        self.assertEquals(expected_object_name, str(model))

    @english
    def test_object_verbose_name_english(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        verbose_name = model._meta.verbose_name
        self.assertEquals(verbose_name, 'reimbursement basic information')

    @finnish
    def test_object_verbose_name_finnish(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        verbose_name = model._meta.verbose_name
        self.assertEquals(verbose_name, 'kulukorvaus perustiedot')

    @english
    def test_object_verbose_name_plural_english(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        verbose_name = model._meta.verbose_name_plural
        self.assertEquals(verbose_name, 'Reimbursement basic information')

    @finnish
    def test_object_verbose_name_plural_finnish(self):
        model = KulukorvausPerustiedot.objects.get(id=1)
        verbose_name = model._meta.verbose_name_plural
        self.assertEquals(verbose_name, 'Kulukorvaus perustiedot')


class KulukorvausModelTest(TestData):
    @english
    def test_created_at_label_english(self):
        model = Kulukorvaus.objects.get(pk=1)
        field_label = model._meta.get_field('created_at').verbose_name
        self.assertEquals(field_label, 'Created at')

    @finnish
    def test_created_at_label_finnish(self):
        model = Kulukorvaus.objects.get(pk=1)
        field_label = model._meta.get_field('created_at').verbose_name
        self.assertEquals(field_label, 'Luotu')

    @english
    def test_target_label_english(self):
        model = Kulukorvaus.objects.get(pk=1)
        field_label = model._meta.get_field('target').verbose_name
        self.assertEquals(field_label, 'Expense explanation')

    @finnish
    def test_target_label_finnish(self):
        model = Kulukorvaus.objects.get(pk=1)
        field_label = model._meta.get_field('target').verbose_name
        self.assertEquals(field_label, 'Kulun selite')

    def test_target_max_length(self):
        model = Kulukorvaus.objects.get(pk=1)
        max_length = model._meta.get_field('target').max_length
        self.assertEquals(max_length, 50)

    @english
    def test_explanation_label_english(self):
        model = Kulukorvaus.objects.get(pk=1)
        field_label = model._meta.get_field('explanation').verbose_name
        self.assertEquals(field_label, 'Event / expense target')

    @finnish
    def test_explanation_label_finnish(self):
        model = Kulukorvaus.objects.get(pk=1)
        field_label = model._meta.get_field('explanation').verbose_name
        self.assertEquals(field_label, 'Tapahtuma / kulun kohde')

    def test_explanation_max_length(self):
        model = Kulukorvaus.objects.get(pk=1)
        max_length = model._meta.get_field('explanation').max_length
        self.assertEquals(max_length, 100)

    @english
    def test_sum_euros_label_english(self):
        model = Kulukorvaus.objects.get(pk=1)
        field_label = model._meta.get_field('sum_euros').verbose_name
        self.assertEquals(field_label, 'Sum (in €)')

    @finnish
    def test_sum_euros_label_finnish(self):
        model = Kulukorvaus.objects.get(pk=1)
        field_label = model._meta.get_field('sum_euros').verbose_name
        self.assertEquals(field_label, 'Summa (euroissa)')

    def test_sum_euros_max_digits_and_decimal_places(self):
        model = Kulukorvaus.objects.get(pk=1)
        max_digits = model._meta.get_field('sum_euros').max_digits
        decimal_places = model._meta.get_field('sum_euros').decimal_places
        self.assertEquals(max_digits, 10)
        self.assertEquals(decimal_places, 2)

    @english
    def test_additional_info_label_english(self):
        model = Kulukorvaus.objects.get(pk=1)
        field_label = model._meta.get_field('additional_info').verbose_name
        self.assertEquals(field_label, 'Additional information')

    @finnish
    def test_additional_info_label_finnish(self):
        model = Kulukorvaus.objects.get(pk=1)
        field_label = model._meta.get_field('additional_info').verbose_name
        self.assertEquals(field_label, 'Lisätietoja, kulujen perusteita')

    @english
    def test_receipt_label_english(self):
        model = Kulukorvaus.objects.get(pk=1)
        field_label = model._meta.get_field('receipt').verbose_name
        self.assertEquals(field_label, 'Receipt')

    @finnish
    def test_receipt_label_finnish(self):
        model = Kulukorvaus.objects.get(pk=1)
        field_label = model._meta.get_field('receipt').verbose_name
        self.assertEquals(field_label, 'Kuitti')

    @english
    def test_object_verbose_name_english(self):
        model = Kulukorvaus.objects.get(pk=1)
        verbose_name = model._meta.verbose_name
        self.assertEquals(verbose_name, 'reimbursement')

    @finnish
    def test_object_verbose_name_finnish(self):
        model = Kulukorvaus.objects.get(pk=1)
        verbose_name = model._meta.verbose_name
        self.assertEquals(verbose_name, 'kulukorvaus')

    @english
    def test_object_verbose_name_plural_english(self):
        model = Kulukorvaus.objects.get(pk=1)
        verbose_name = model._meta.verbose_name_plural
        self.assertEquals(verbose_name, 'Reimbursements')

    @finnish
    def test_object_verbose_name_plural_finnish(self):
        model = Kulukorvaus.objects.get(pk=1)
        verbose_name = model._meta.verbose_name_plural
        self.assertEquals(verbose_name, 'Kulukorvaukset')

    def test_get_absolute_url(self):
        model = Kulukorvaus.objects.get(pk=1)
        # This will also fail if the urlconf is not defined.
        self.assertEquals(model.get_absolute_url(
        ), "kulukorvaukset/{}/{}".format(model.created_at.year, model.pk))
