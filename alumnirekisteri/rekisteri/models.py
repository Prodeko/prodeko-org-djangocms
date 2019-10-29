# from audit_log.models.managers import AuditLog
import datetime
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.db.models import Q
from django.template.defaultfilters import slugify

# Create your models here.


class MailList(models.Model):
    title = models.CharField(max_length=250)
    address = models.CharField(max_length=250)


class Person(models.Model):
    GENDER_CHOICES = ((0, "Mies"), (1, "Nainen"), (2, "Muu"))
    MARITAL_CHOICES = (
        (0, "Avioliitossa"),
        (1, "Naimaton"),
        (2, "Avoliitto"),
        (3, "Rekisteröity parisuhde"),
        (4, "Leski"),
        (5, "Eronnut"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    is_hidden = models.BooleanField(default=False)

    """name settings"""
    middle_names = models.CharField(max_length=250, blank=True, null=True)
    original_last_name = models.CharField(max_length=250, blank=True, null=True)
    nickname = models.CharField(max_length=250, blank=True, null=True)
    preferred_name = models.CharField(max_length=250, null=True, blank=True)
    show_name_category = models.BooleanField(blank=False, default=True)

    picture = models.FileField(upload_to="profiles", blank=True, null=True)

    """address"""
    address = models.CharField(max_length=500, null=True, blank=True)
    postal_code = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=250, null=True, blank=True)
    country = models.CharField(max_length=250, null=True, blank=True)
    show_address_category = models.BooleanField(blank=False, default=True)

    """personal"""
    birthdate = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=250, null=True, blank=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, null=True, blank=True)
    marital_status = models.IntegerField(blank=True, null=True, choices=MARITAL_CHOICES)
    show_personal_category = models.BooleanField(blank=False, default=True)

    """military"""
    military_rank = models.CharField(max_length=250, blank=True, null=True)
    promotion_year = models.IntegerField(blank=True, null=True)
    show_military_category = models.BooleanField(blank=False, default=True)

    """ Prodeko info """
    MEMBERTYPE_CHOICES = (
        (0, "None"),
        (1, "Varsinainen"),
        (2, "Ulkojäsen"),
        (3, "Vanha jäsen"),
        (4, "Kannatusjäsen"),
        (5, "Kunniajäsen"),
    )
    class_of_year = models.IntegerField(null=True, blank=True)
    xq_year = models.IntegerField(null=True, blank=True)
    member_until = models.DateField(null=True, blank=True)
    member_type = models.IntegerField(null=True, choices=MEMBERTYPE_CHOICES)
    ayy_member = models.BooleanField(blank=False, default=False)

    """private info"""
    student_number = models.CharField(max_length=50, blank=True, null=True)
    subscribed_lists = models.ManyToManyField(MailList, blank=True)
    dont_publish_in_book = models.NullBooleanField(null=True, blank=True, default=False)
    mentoring = models.NullBooleanField(null=True, blank=True, default=False)
    upper_management_mentoring = models.NullBooleanField(
        null=True, blank=True, default=False
    )
    ventures = models.NullBooleanField(null=True, blank=True, default=False)
    partner_contact = models.NullBooleanField(null=True, blank=True, default=False)
    is_alumni = models.NullBooleanField(null=True, blank=True)
    is_dead = models.NullBooleanField(null=True, blank=True, default=False)
    subscribe_alumnimail = models.NullBooleanField(null=True, blank=True, default=False)
    admin_note = models.CharField(max_length=1000, blank=True, null=True)

    """contact info"""
    homepage = models.CharField(max_length=250, blank=True, null=True)
    show_email_address = models.BooleanField(blank=False, default=True)
    linkedin_profile = models.CharField(max_length=250, null=True, blank=True)
    show_contact_category = models.BooleanField(blank=False, default=False)

    show_phones_category = models.BooleanField(blank=False, default=False)
    show_emails_category = models.BooleanField(blank=False, default=False)
    show_skills_category = models.BooleanField(blank=False, default=False)
    show_languages_category = models.BooleanField(blank=False, default=False)
    show_educations_category = models.BooleanField(blank=False, default=False)
    show_work_experiences_category = models.BooleanField(blank=False, default=False)
    show_positions_of_trust_category = models.BooleanField(blank=False, default=False)
    show_volunteers_category = models.BooleanField(blank=False, default=False)
    show_honors_category = models.BooleanField(blank=False, default=False)
    show_interests_category = models.BooleanField(blank=False, default=False)
    show_student_organizational_activities_category = models.BooleanField(
        blank=False, default=False
    )
    show_family_members_category = models.BooleanField(blank=False, default=False)

    """industries"""
    industry_consulting = models.BooleanField(blank=False, default=False)
    industry_industrial = models.BooleanField(blank=False, default=False)
    industry_law = models.BooleanField(blank=False, default=False)
    industry_consumer = models.BooleanField(blank=False, default=False)
    industry_health = models.BooleanField(blank=False, default=False)
    industry_energy = models.BooleanField(blank=False, default=False)
    industry_it = models.BooleanField(blank=False, default=False)
    industry_finance = models.BooleanField(blank=False, default=False)
    industry_traffic = models.BooleanField(blank=False, default=False)
    industry_retail = models.BooleanField(blank=False, default=False)
    industry_media = models.BooleanField(blank=False, default=False)
    industry_marketing = models.BooleanField(blank=False, default=False)

    """functions"""
    function_logistics = models.BooleanField(blank=False, default=False)
    function_ackquisitions = models.BooleanField(blank=False, default=False)
    function_sales = models.BooleanField(blank=False, default=False)
    function_digital_marketing = models.BooleanField(blank=False, default=False)
    function_marketing = models.BooleanField(blank=False, default=False)
    function_pr = models.BooleanField(blank=False, default=False)
    function_hr = models.BooleanField(blank=False, default=False)
    function_rnd = models.BooleanField(blank=False, default=False)
    function_finance = models.BooleanField(blank=False, default=False)
    function_it = models.BooleanField(blank=False, default=False)
    function_ux = models.BooleanField(blank=False, default=False)
    function_analytics = models.BooleanField(blank=False, default=False)
    function_strategy = models.BooleanField(blank=False, default=False)
    function_enterpreneurship = models.BooleanField(blank=False, default=False)
    function_research = models.BooleanField(blank=False, default=False)
    function_free = models.CharField(max_length=1000, blank=True, null=True)

    slug = models.CharField(max_length=255, unique=True, null=True)

    """ audit_log = AuditLog() """

    def __str__(self):
        nickname = ""
        first_name = "Etu"
        last_name = "Suku"
        if self.user:
            first_name = self.user.first_name
            last_name = self.user.last_name
        if self.nickname:
            nickname = '"' + self.nickname + '" '
        if self.preferred_name:
            first_name = self.preferred_name
        return first_name + " " + nickname + last_name

    def fullname(self):
        return self.user.first_name + " " + self.user.last_name

    def save(self, *args, **kwargs):
        if self.slug is None:
            slug = slugify(str(self))
            duplicate_slug = Person.objects.filter(slug=slug).count() > 0
            counter = 0
            while duplicate_slug:
                counter += 1
                slug = slugify(str(self)) + "-" + str(counter)
                if Person.objects.filter(slug=slug).count() == 0:
                    duplicate_slug = False
            self.slug = slug
        super(Person, self).save(*args, **kwargs)

    def get_starting_year(self):
        e = (
            self.get_tuta_educations()
            .filter(~Q(degree_level=5))
            .exclude(end_year__isnull=True)
        )

        def sortByStartDate(x):
            return (x.start_year if x.start_year else 0) * 12 + (
                x.start_month if hasattr(x, "end_month") and x.start_month else 0
            )

        if e.count() > 0:
            return sorted(e, key=sortByStartDate)[0].start_year
        else:
            return "-"

    def get_graduation_year(self):
        e = (
            self.get_tuta_educations()
            .filter(~Q(degree_level=5))
            .exclude(end_year__isnull=True)
        )

        def sortByEndDate(x):
            return -(
                (x.end_year if x.end_year else 0) * 12
                + (x.end_month if hasattr(x, "end_month") and x.end_month else 0)
            )

        if e.count() > 0:
            return sorted(e, key=sortByEndDate)[0].end_year
        else:
            return "-"

    def is_tuta_doctor(self):
        e_count = self.get_tuta_educations().filter(Q(degree_level=5)).count()
        return e_count > 0

    def is_tuta_lisensiaatti(self):
        e_count = self.get_tuta_educations().filter(Q(degree_level=4)).count()
        return e_count > 0

    def get_tuta_educations(self):
        return (
            self.educations.filter(
                Q(school__iexact="TKK")
                | Q(school__iexact="STKK")
                | Q(school__icontains="Suomen teknillinen korkeakoulu")
                | Q(school__iexact="AY")
                | Q(school__icontains="Aalto")
                | Q(school__icontains="Helsinki University of Technology")
                | Q(school__iexact="Teknillinen korkeakoulu")
                | Q(school__icontains="HUT")
            )
            .filter(
                ~Q(field__icontains="Kauppakorkea")
                & ~Q(major__icontains="Kauppakorkea")
            )
            .filter(
                Q(field__iexact="Tu")
                | Q(major__iexact="Tu")
                | Q(field__icontains="tuotantotalo")
                | Q(field__icontains="teollisuustalo")
                | Q(major__icontains="teollisuustalo")
                | Q(field__icontains="tietojenkäsittelyoppi")
                | Q(major__icontains="tietojenkäsittelyoppi")
                | Q(field__icontains="työpsyko")
                | Q(major__icontains="työpsyko")
                | Q(field__icontains="tuotantostra")
                | Q(major__icontains="tuotantostra")
                | Q(field__icontains="logistiikka")
                | Q(major__icontains="logistiikka")
                | Q(field__icontains="palvelutuotanto")
                | Q(major__icontains="palvelutuotanto")
                | Q(field__icontains="industrial e")
                | Q(major__icontains="industrial e")
                | Q(field__icontains="strategi")
                | Q(major__icontains="strategi")
                | Q(field__icontains="projektiliiketoiminta")
                | Q(major__icontains="projektiliiketoiminta")
                | Q(field__icontains="organisaatiot ja johtaminen")
                | Q(major__icontains="organisaatiot ja johtaminen")
                | Q(major__icontains="tuotantotalo")
            )
        )

    def get_absolute_url(self):
        return reverse("alumnirekisteri:public_profile", args=[self.slug])

    def get_picture_url(self):
        if self.picture:
            return self.picture.url
        return "/static/alumnirekisteri_images/no_profile.jpg"

    def get_name_info(self):
        info = {}
        if self.show_name_category:
            info["Alkuperäinen sukunimi"] = self.original_last_name
            info["Lempinimi"] = self.nickname
            info["Kutsumanimi"] = self.preferred_name
        return dict((k, v) for k, v in info.items() if v)

    def get_personal(self):
        info = {}
        if self.show_personal_category:
            info["Syntymäpäivä"] = self.birthdate
            info["Sukupuoli"] = self.get_gender_display()
            info["Siviilisääty"] = self.get_marital_status_display()
        return dict((k, v) for k, v in info.items() if v)

    def get_address(self):
        info = {}
        if self.show_address_category:
            info["Osoite"] = self.address
            info["Postinumero"] = self.postal_code
            info["Kaupunki"] = self.city
            info["Maa"] = self.country
        return dict((k, v) for k, v in info.items() if v)

    def get_military(self):
        info = {}
        if self.show_military_category:
            info["Sotilasarvo"] = self.military_rank
            info["Ylennysvuosi"] = self.promotion_year
        return dict((k, v) for k, v in info.items() if v)

    def get_contact(self):
        info = {}
        if self.show_email_address:
            info["Sähköposti"] = self.user.email
        if self.show_contact_category:
            info["Kotisivu"] = self.homepage
            info["LinkedIn"] = self.linkedin_profile
        return dict((k, v) for k, v in info.items() if v)

    def is_foreign(self):
        if self.country:
            return self.country.lower() != "finland" or self.country.lower() != "Suomi"
        else:
            return False

    def get_family_members_sorted(self):
        return sorted(
            self.family_members.all(),
            key=lambda x: [3, 4, 0, 1, 2].index(x.member_type),
        )


class Phone(models.Model):
    NUMBER_TYPE_CHOICES = (("P", "Henkilökohtainen"), ("W", "Työ"))
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="phones")
    phone_number = models.CharField(max_length=250)
    number_type = models.CharField(max_length=1, choices=NUMBER_TYPE_CHOICES)

    """ audit_log = AuditLog() """


class Email(models.Model):
    ADDRESS_TYPE_CHOICES = (("P", "Henkilökohtainen"), ("W", "Työ"))
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="emails")
    address = models.EmailField(max_length=250)
    address_type = models.CharField(max_length=1, choices=ADDRESS_TYPE_CHOICES)

    """ audit_log = AuditLog() """


class Skill(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="skills")
    title = models.CharField(max_length=250)
    description = models.TextField()

    """ audit_log = AuditLog() """


class Language(models.Model):
    LEVEL_CHOICES = (
        (0, "Äidinkieli"),
        (1, "Erinomainen"),
        (2, "Hyvä"),
        (3, "Tyydyttävä"),
        (4, "Alkeet"),
    )
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="languages"
    )
    language = models.CharField(max_length=250)
    level = models.IntegerField(null=True, blank=True, choices=LEVEL_CHOICES)

    """ audit_log = AuditLog() """


class Education(models.Model):
    DEGREE_CHOICES = (
        (0, "Luokittelematon"),
        (1, "Toisen asteen tutkinto"),
        (2, "Alempi korkeakoulututkinto"),
        (3, "Ylempi korkeakoulututkinto"),
        (4, "Lisensiaatti"),
        (5, "Tohtori"),
        (6, "Dosentti"),
    )
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="educations"
    )
    school = models.CharField(max_length=250)
    field = models.CharField(max_length=250, blank=True)
    degree_level = models.IntegerField(null=True, blank=True, choices=DEGREE_CHOICES)
    major = models.CharField(max_length=250, blank=True)
    minor = models.CharField(max_length=250, blank=True)
    start_year = models.IntegerField(null=True, blank=True)
    end_year = models.IntegerField(null=True, blank=True)
    description = models.TextField(max_length=500, blank=True, null=True)

    """ audit_log = AuditLog() """


class WorkExperience(models.Model):
    MONTH_CHOICES = (
        (0, "Tammikuu"),
        (1, "Helmikuu"),
        (2, "Maaliskuu"),
        (3, "Huhtikuu"),
        (4, "Toukokuu"),
        (5, "Kesäkuu"),
        (6, "Heinäkuu"),
        (7, "Elokuu"),
        (8, "Syyskuu"),
        (9, "Lokakuu"),
        (10, "Marraskuu"),
        (11, "Joulukuu"),
    )
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="work_experiences"
    )
    organisation = models.CharField(max_length=250)
    position = models.CharField(max_length=250)
    start_year = models.IntegerField(blank=True, null=True)
    start_month = models.IntegerField(blank=True, null=True, choices=MONTH_CHOICES)
    end_year = models.IntegerField(blank=True, null=True)
    end_month = models.IntegerField(blank=True, null=True, choices=MONTH_CHOICES)
    description = models.CharField(blank=True, max_length=1000)
    """address"""
    address = models.CharField(max_length=500, null=True, blank=True)
    postal_code = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=250, null=True, blank=True)
    country = models.CharField(max_length=250, null=True, blank=True)
    show_address_category = models.BooleanField(blank=False, default=True)

    """ audit_log = AuditLog() """


class PositionOfTrust(models.Model):
    MONTH_CHOICES = (
        (0, "Tammikuu"),
        (1, "Helmikuu"),
        (2, "Maaliskuu"),
        (3, "Huhtikuu"),
        (4, "Toukokuu"),
        (5, "Kesäkuu"),
        (6, "Heinäkuu"),
        (7, "Elokuu"),
        (8, "Syyskuu"),
        (9, "Lokakuu"),
        (10, "Marraskuu"),
        (11, "Joulukuu"),
    )
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="positions_of_trust"
    )
    organisation = models.CharField(max_length=250)
    position = models.CharField(max_length=250)
    start_year = models.IntegerField(blank=True, null=True)
    start_month = models.IntegerField(blank=True, null=True, choices=MONTH_CHOICES)
    end_year = models.IntegerField(blank=True, null=True)
    end_month = models.IntegerField(blank=True, null=True, choices=MONTH_CHOICES)
    description = models.CharField(max_length=1000, blank=True)

    """ audit_log = AuditLog() """


class StudentOrganizationalActivity(models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="student_organizational_activities",
    )
    organisation = models.CharField(max_length=250)
    position = models.CharField(max_length=250)
    start_year = models.IntegerField(null=True, blank=True)
    end_year = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True)

    """ audit_log = AuditLog() """


class Volunteer(models.Model):
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="volunteers"
    )
    organisation = models.CharField(max_length=250)
    position = models.CharField(max_length=250)
    start_year = models.IntegerField(blank=True, null=True)
    end_year = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)

    """ audit_log = AuditLog() """

    def ___str___(self):
        return (self.organisation, self.position)


class Honor(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="honors")
    title = models.CharField(max_length=250)
    year = models.IntegerField(blank=True, null=True)
    organisation = models.CharField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)

    """ audit_log = AuditLog() """

    def ___str___(self):
        return self.title


class Interest(models.Model):
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="interests"
    )
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=2000, blank=True, null=True)

    """ audit_log = AuditLog() """

    def ___str___(self):
        return self.title


class FamilyMember(models.Model):
    MEMBERTYPE_CHOICES = (
        (0, "Lapsi"),
        (1, "Vanhempi"),
        (2, "Sisarus"),
        (3, "Puoliso"),
        (4, "Avopuoliso"),
    )
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name="family_members"
    )
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    original_last_name = models.CharField(max_length=250, blank=True, null=True)
    since = models.IntegerField(blank=True, null=True)
    until = models.IntegerField(blank=True, null=True)
    member_type = models.IntegerField(null=True, choices=MEMBERTYPE_CHOICES)
    profession = models.CharField(max_length=250, null=True, blank=True)

    """ audit_log = AuditLog() """

    def ___str___(self):
        return (self.first_name, self.last_name)

    def get_full_name(self):
        return self.first_name, self.last_name
