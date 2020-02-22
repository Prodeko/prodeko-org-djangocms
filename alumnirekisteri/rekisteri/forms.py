from django import forms

from alumnirekisteri.auth2.forms import RegisterForm as auth2RegisterForm
from alumnirekisteri.rekisteri.models import *
from auth_prodeko.models import User


class RegisterForm(auth2RegisterForm):

    first_name = forms.CharField(
        label="Etunimi",
        widget=forms.DateInput(
            attrs={"class": "form-control datepicker", "required": "required"}
        ),
    )
    middle_names = forms.CharField(
        label="Toiset nimet",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )
    last_name = forms.CharField(
        label="Sukunimi",
        widget=forms.DateInput(
            attrs={"class": "form-control datepicker", "required": "required"}
        ),
    )

    city = forms.CharField(
        label="Kaupunki",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )
    country = forms.CharField(
        label="Maa",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )
    member_until = forms.CharField(
        label="Jäsenyys päättyy",
        widget=forms.DateInput(attrs={"class": "form-control"}),
        required=False,
    )
    class_of_year = forms.IntegerField(
        label="Vuosikurssi",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        required=False,
    )
    xq_year = forms.IntegerField(
        label="XQ Vuosikurssi",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        required=False,
    )
    ayy_member = forms.BooleanField(
        label="AYY Jäsen",
        widget=forms.CheckboxInput(attrs={"class": "form-control"}),
        required=False,
    )

    member_type = forms.ChoiceField(
        widget=forms.Select(),
        choices=Person.MEMBERTYPE_CHOICES,
        label="Käyttäjätyyppi",
        required=True,
    )

    def is_valid(self):
        valid = super(RegisterForm, self).is_valid()
        if not valid:
            return False
        return True

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            person = Person.objects.create(user=user)
            person.middle_names = self.cleaned_data["middle_names"]
            person.city = self.cleaned_data["city"]
            person.country = self.cleaned_data["country"]
            person.member_until = self.cleaned_data["member_until"]
            person.class_of_year = self.cleaned_data["class_of_year"]
            person.xq_year = self.cleaned_data["xq_year"]
            person.ayy_member = self.cleaned_data["ayy_member"]
            person.member_type = self.cleaned_data["member_type"]
            person.save()
        return user, person


class UserForm(forms.ModelForm):
    """ Edit User model fields """

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "email": "Sähköpostiosoite *",
            "first_name": "Etunimi *",
            "last_name": "Sukunimi *",
        }


class AdminPersonForm(forms.ModelForm):
    """ Edit person model fields that are only accessible to admin """

    class Meta:
        model = Person
        fields = [
            "admin_note",
            "member_until",
            "is_alumni",
            "is_dead",
            "xq_year",
            "ayy_member",
            "member_type",
        ]
        widgets = {
            "admin_note": forms.TextInput(attrs={"class": "form-control"}),
            "member_until": forms.TextInput(attrs={"class": "form-control"}),
            "is_alumni": forms.CheckboxInput(
                attrs={
                    "data-toggle": "toggle",
                    "data-on": "Alumni",
                    "data-off": "Kiltalainen",
                    "data-size": "mini",
                }
            ),
            "is_dead": forms.CheckboxInput(
                attrs={
                    "data-toggle": "toggle",
                    "data-on": "Kuollut",
                    "data-off": "Elossa",
                    "data-size": "mini",
                }
            ),
            "xq_year": forms.NumberInput(attrs={"class": "form-control"}),
            "ayy_member": forms.CheckboxInput(
                attrs={
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "member_type": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "admin_note": "Ylläpitäjän muistiinpano",
            "member_until": "Prodekon jäsenyys päättyy",
            "is_alumni": "Alumni",
            "is_dead": "Kuollut",
            "xq_year": "XQ-vuosikurssi",
            "ayy_member": "AYY:n jäsen",
            "member_type": "Jäsenyystyyppi",
        }


class PersonForm(forms.ModelForm):
    """ Edit Person fields """

    class Meta:
        model = Person
        fields = [
            "original_last_name",
            "middle_names",
            "nickname",
            "preferred_name",
            "show_name_category",
            "show_contact_category",
            "address",
            "postal_code",
            "city",
            "country",
            "show_address_category",
            "birthdate",
            "gender",
            "marital_status",
            "show_personal_category",
            "military_rank",
            "promotion_year",
            "show_military_category",
            "class_of_year",
            "student_number",
            "dont_publish_in_book",
            "mentoring",
            "upper_management_mentoring",
            "ventures",
            "partner_contact",
            "subscribe_alumnimail",
            "homepage",
            "linkedin_profile",
            "show_email_address",
            "show_phones_category",
            "show_emails_category",
            "show_skills_category",
            "show_languages_category",
            "show_educations_category",
            "show_work_experiences_category",
            "show_positions_of_trust_category",
            "show_volunteers_category",
            "show_honors_category",
            "show_interests_category",
            "show_student_organizational_activities_category",
            "show_family_members_category",
            "industry_consulting",
            "industry_industrial",
            "industry_law",
            "industry_consumer",
            "industry_health",
            "industry_energy",
            "industry_it",
            "industry_finance",
            "industry_traffic",
            "industry_retail",
            "industry_media",
            "industry_marketing",
            "function_logistics",
            "function_ackquisitions",
            "function_sales",
            "function_digital_marketing",
            "function_marketing",
            "function_pr",
            "function_hr",
            "function_rnd",
            "function_finance",
            "function_it",
            "function_ux",
            "function_analytics",
            "function_strategy",
            "function_enterpreneurship",
            "function_research",
            "function_free",
        ]
        widgets = {
            "original_last_name": forms.TextInput(attrs={"class": "form-control"}),
            "middle_names": forms.TextInput(attrs={"class": "form-control"}),
            "nickname": forms.TextInput(attrs={"class": "form-control"}),
            "preferred_name": forms.TextInput(attrs={"class": "form-control"}),
            "show_name_category": forms.CheckboxInput(
                attrs={
                    "class": "category-checkbox",
                    "data-toggle": "toggle",
                    "data-on": "Julkinen",
                    "data-off": "Yksityinen",
                    "data-size": "mini",
                }
            ),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "postal_code": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
            "show_address_category": forms.CheckboxInput(
                attrs={
                    "class": "category-checkbox",
                    "data-toggle": "toggle",
                    "data-on": "Julkinen",
                    "data-off": "Yksityinen",
                    "data-size": "mini",
                }
            ),
            "birthdate": forms.TextInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "marital_status": forms.Select(attrs={"class": "form-control"}),
            "show_personal_category": forms.CheckboxInput(
                attrs={
                    "class": "category-checkbox",
                    "data-toggle": "toggle",
                    "data-on": "Julkinen",
                    "data-off": "Yksityinen",
                    "data-size": "mini",
                }
            ),
            "military_rank": forms.TextInput(attrs={"class": "form-control"}),
            "promotion_year": forms.TextInput(attrs={"class": "form-control"}),
            "show_military_category": forms.CheckboxInput(
                attrs={
                    "class": "category-checkbox",
                    "data-toggle": "toggle",
                    "data-on": "Julkinen",
                    "data-off": "Yksityinen",
                    "data-size": "mini",
                }
            ),
            "class_of_year": forms.NumberInput(attrs={"class": "form-control"}),
            "student_number": forms.TextInput(attrs={"class": "form-control"}),
            "dont_publish_in_book": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "mentoring": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "upper_management_mentoring": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "ventures": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "partner_contact": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "subscribe_alumnimail": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "homepage": forms.URLInput(attrs={"class": "form-control"}),
            "linkedin_profile": forms.URLInput(attrs={"class": "form-control"}),
            "show_email_address": forms.CheckboxInput(
                attrs={
                    "class": "category-checkbox",
                    "data-toggle": "toggle",
                    "data-on": "Julkinen",
                    "data-off": "Yksityinen",
                    "data-size": "mini",
                }
            ),
            "show_contact_category": forms.CheckboxInput(
                attrs={
                    "class": "category-checkbox",
                    "data-toggle": "toggle",
                    "data-on": "Julkinen",
                    "data-off": "Yksityinen",
                    "data-size": "mini",
                }
            ),
            "show_phones_category": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Julkinen",
                    "data-off": "Yksityinen",
                    "data-size": "mini",
                }
            ),
            "show_emails_category": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Julkinen",
                    "data-off": "Yksityinen",
                    "data-size": "mini",
                }
            ),
            "show_skills_category": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Julkinen",
                    "data-off": "Yksityinen",
                    "data-size": "mini",
                }
            ),
            "show_languages_category": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Julkinen",
                    "data-off": "Yksityinen",
                    "data-size": "mini",
                }
            ),
            "show_educations_category": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Julkinen",
                    "data-off": "Yksityinen",
                    "data-size": "mini",
                }
            ),
            "show_work_experiences_category": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Julkinen",
                    "data-off": "Yksityinen",
                    "data-size": "mini",
                }
            ),
            "show_positions_of_trust_category": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Julkinen",
                    "data-off": "Yksityinen",
                    "data-size": "mini",
                }
            ),
            "show_volunteers_category": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Julkinen",
                    "data-off": "Yksityinen",
                    "data-size": "mini",
                }
            ),
            "show_honors_category": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Julkinen",
                    "data-off": "Yksityinen",
                    "data-size": "mini",
                }
            ),
            "show_interests_category": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Julkinen",
                    "data-off": "Yksityinen",
                    "data-size": "mini",
                }
            ),
            "show_student_organizational_activities_category": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Julkinen",
                    "data-off": "Yksityinen",
                    "data-size": "mini",
                }
            ),
            "show_family_members_category": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Julkinen",
                    "data-off": "Yksityinen",
                    "data-size": "mini",
                }
            ),
            "industry_consulting": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "industry_industrial": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "industry_law": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "industry_consumer": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "industry_health": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "industry_energy": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "industry_it": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "industry_finance": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "industry_traffic": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "industry_retail": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "industry_media": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "industry_marketing": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "function_logistics": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "function_ackquisitions": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "function_sales": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "function_digital_marketing": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "function_marketing": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "function_pr": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "function_hr": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "function_rnd": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "function_finance": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "function_it": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "function_ux": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "function_analytics": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "function_strategy": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "function_enterpreneurship": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "function_research": forms.CheckboxInput(
                attrs={
                    "class": "",
                    "data-toggle": "toggle",
                    "data-on": "Kyllä",
                    "data-off": "Ei",
                    "data-size": "mini",
                }
            ),
            "function_free": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }
        labels = {
            "original_last_name": "Alkuperäinen sukunimi",
            "middle_names": "Toiset nimet",
            "nickname": "Lempinimi",
            "preferred_name": "Kutsumanimi",
            "show_name_category": "Näytä tiedot muille käyttäjille",
            "address": "Osoite",
            "postal_code": "Postinumero",
            "city": "Kaupunki",
            "country": "Maa",
            "show_address_category": "Näytä tiedot muille käyttäjille",
            "birthdate": "Syntymäpäivä",
            "gender": "Sukupuoli",
            "marital_status": "Siviilisääty",
            "show_personal_category": "Näytä tiedot muille käyttäjille",
            "military_rank": "Sotilasarvo",
            "promotion_year": "Ylennysvuosi",
            "show_military_category": "Näytä tiedot muille käyttäjille",
            "homepage": "Kotisivu",
            "linkedin_profile": "LinkedIn",
            "show_email_address": "Näytä sähköposti muille käyttäjille",
            "class_of_year": "Vuosikurssi",
            "student_number": "Opiskelijanumero",
            "dont_publish_in_book": "Kiellän tietojeni julkaisemisen matrikkelissa",
            "mentoring": "Olen käytettävissä kiltamentorointiin (1-2 kertaa vuodessa)",
            "upper_management_mentoring": "Olen kiinnostunut ylimmän johdon mentorointitoimeksiannoista (Prodeko Ventures)",
            "subscribe_alumnimail": "Tilaa alumnikirje",
            "ventures": "Minuun saa olla yhteydessä Prodeko Venturesin neuvonantajarooleista",
            "partner_contact": "Yhteystietoni saa luovuttaa Prodeko Alumnin yhteistyökumppaneille (esim. aTalent)",
            "show_contact_category": "Näytä tiedot muille käyttäjille",
            "show_phones_category": "Näytä tiedot muille käyttäjille",
            "show_emails_category": "Näytä tiedot muille käyttäjille",
            "show_skills_category": "Näytä tiedot muille käyttäjille",
            "show_languages_category": "Näytä tiedot muille käyttäjille",
            "show_educations_category": "Näytä tiedot muille käyttäjille",
            "show_work_experiences_category": "Näytä tiedot muille käyttäjille",
            "show_positions_of_trust_category": "Näytä tiedot muille käyttäjille",
            "show_volunteers_category": "Näytä tiedot muille käyttäjille",
            "show_honors_category": "Näytä tiedot muille käyttäjille",
            "show_interests_category": "Näytä tiedot muille käyttäjille",
            "show_student_organizational_activities_category": "Näytä tiedot muille käyttäjille",
            "show_family_members_category": "Näytä tiedot muille käyttäjille",
            "industry_consulting": "Konsultointi",
            "industry_industrial": "Teollisuus",
            "industry_law": "Juridiikka",
            "industry_consumer": "Kuluttajatuotteet / Palvelut",
            "industry_health": "Terveys ja hyvinvointi + healthtech",
            "industry_energy": "Energia / Clean tech",
            "industry_it": "Ohjelmistot / IT-palvelut",
            "industry_finance": "Finanssipalvelut / Vakuutus / VC + fintech",
            "industry_traffic": "Liikenne",
            "industry_retail": "Vähittäiskauppa (retail)",
            "industry_media": "Media ja verkkojulkaisut + adtech",
            "industry_marketing": "Mainonta",
            "function_logistics": "Tuotanto / logistiikka",
            "function_ackquisitions": "Hankinnat",
            "function_sales": "Myynti",
            "function_digital_marketing": "Digimarkkinointi",
            "function_marketing": "Markkinointi",
            "function_pr": "Viestintä",
            "function_hr": "HR",
            "function_rnd": "Tuotekehitys",
            "function_finance": "Finanssi / Talous",
            "function_it": "IT",
            "function_ux": "Design / UX",
            "function_analytics": "Analytiikka",
            "function_strategy": "Strategia",
            "function_enterpreneurship": "Yrittäjyys",
            "function_research": "Akateeminen tutkimus",
            "function_free": "Tarkennus/muu, esim. AI, kansainvälistyminen, mobiilisofta, rahoituskierrokset, yrityskaupat",
        }


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ["phone_number", "number_type"]
        widgets = {
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "number_type": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {"phone_number": "Puhelinnumero", "number_type": "Tyyppi"}


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ["address", "address_type"]
        widgets = {
            "address": forms.EmailInput(attrs={"class": "form-control"}),
            "address_type": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {"address": "Sähköpostiosoite", "address_type": "Tyyppi"}


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {"title": "Erityistaito", "description": "Kuvaus"}


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ["language", "level"]
        widgets = {
            "language": forms.TextInput(attrs={"class": "form-control"}),
            "level": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {"language": "Kieli", "level": "Taso"}


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = [
            "school",
            "field",
            "degree_level",
            "major",
            "minor",
            "start_year",
            "end_year",
            "description",
        ]
        widgets = {
            "school": forms.TextInput(attrs={"class": "form-control"}),
            "field": forms.TextInput(attrs={"class": "form-control"}),
            "degree_level": forms.Select(attrs={"class": "form-control"}),
            "major": forms.TextInput(attrs={"class": "form-control"}),
            "minor": forms.TextInput(attrs={"class": "form-control"}),
            "start_year": forms.TextInput(attrs={"class": "form-control"}),
            "end_year": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "school": "Koulu",
            "field": "Ala",
            "degree_level": "Tutkintoaste",
            "major": "Pääaine",
            "minor": "Sivuaine",
            "start_year": "Aloitusvuosi",
            "end_year": "Lopetusvuosi",
            "description": "Kuvaus",
        }


class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = [
            "organisation",
            "position",
            "start_year",
            "start_month",
            "end_year",
            "end_month",
            "description",
            "address",
            "postal_code",
            "city",
            "country",
        ]
        widgets = {
            "organisation": forms.TextInput(attrs={"class": "form-control"}),
            "position": forms.TextInput(attrs={"class": "form-control"}),
            "start_year": forms.NumberInput(attrs={"class": "form-control"}),
            "start_month": forms.Select(attrs={"class": "form-control"}),
            "end_year": forms.NumberInput(attrs={"class": "form-control"}),
            "end_month": forms.Select(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "postal_code": forms.NumberInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "organisation": "Organisaatio",
            "position": "Positio",
            "start_year": "Aloitusvuosi",
            "start_month": "Aloituskuukausi",
            "end_year": "Lopetusvuosi",
            "end_month": "Lopetuskuukausi",
            "description": "Kuvaus",
            "address": "Osoite",
            "postal_code": "Postinumero",
            "city": "Kaupunki",
            "country": "Maa",
        }


class PositionOfTrustForm(forms.ModelForm):
    class Meta:
        model = PositionOfTrust
        fields = [
            "organisation",
            "position",
            "start_year",
            "start_month",
            "end_year",
            "end_month",
            "description",
        ]
        widgets = {
            "organisation": forms.TextInput(attrs={"class": "form-control"}),
            "position": forms.TextInput(attrs={"class": "form-control"}),
            "start_year": forms.NumberInput(attrs={"class": "form-control"}),
            "start_month": forms.Select(attrs={"class": "form-control"}),
            "end_year": forms.NumberInput(attrs={"class": "form-control"}),
            "end_month": forms.Select(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "organisation": "Organisaatio",
            "position": "Positio",
            "start_year": "Aloitusvuosi",
            "start_month": "Aloituskuukausi",
            "end_year": "Lopetusvuosi",
            "end_month": "Lopetuskuukausi",
            "description": "Kuvaus",
        }


class StudentActivityForm(forms.ModelForm):
    class Meta:
        model = StudentOrganizationalActivity
        fields = ["organisation", "position", "start_year", "end_year", "description"]
        widgets = {
            "organisation": forms.TextInput(attrs={"class": "form-control"}),
            "position": forms.TextInput(attrs={"class": "form-control"}),
            "start_year": forms.NumberInput(attrs={"class": "form-control"}),
            "end_year": forms.NumberInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "organisation": "Organisaatio",
            "position": "Positio",
            "start_year": "Aloitusvuosi",
            "end_year": "Lopetusvuosi",
            "description": "Kuvaus",
        }


class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ["organisation", "position", "start_year", "end_year", "description"]
        widgets = {
            "organisation": forms.TextInput(attrs={"class": "form-control"}),
            "position": forms.TextInput(attrs={"class": "form-control"}),
            "start_year": forms.NumberInput(attrs={"class": "form-control"}),
            "end_year": forms.NumberInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "organisation": "Organisaatio",
            "position": "Positio",
            "start_year": "Aloitusvuosi",
            "end_year": "Lopetusvuosi",
            "description": "Kuvaus",
        }


class HonorForm(forms.ModelForm):
    class Meta:
        model = Honor
        fields = ["title", "year", "organisation", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "organisation": forms.TextInput(attrs={"class": "form-control"}),
            "year": forms.NumberInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "title": "Nimi",
            "organisation": "Organisaatio",
            "year": "Vuosi",
            "description": "Kuvaus",
        }


class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {"title": "Nimi", "description": "Kuvaus"}


class FamilyMemberForm(forms.ModelForm):
    class Meta:
        model = FamilyMember
        fields = ["first_name", "last_name", "original_last_name", "member_type"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "original_last_name": forms.TextInput(attrs={"class": "form-control"}),
            "member_type": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "first_name": "Etunimi",
            "last_name": "Sukunimi",
            "original_last_name": "Alkuperäinen sukunimi",
            "member_type": "Tyyppi",
        }
