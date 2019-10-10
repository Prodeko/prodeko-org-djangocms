import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Message(models.Model):
    """Basic information about the reimbursement claim as a whole.

    The Message model represents a message sent through
    the contact form.

    Attributes:
        created_at: Timestamp of object creation.
        email: Email address.
        message: The contact message content.
    """

    CONTACT_EMAILS = [
        (
            "YA",
            "hallitus@prodeko.org",
            _("Feedback and general questions (hallitus@prodeko.org)"),
        ),
        (
            "PT",
            "hallitus@prodeko.org",
            _(
                "PTER (Prodekoian activities encouragement fund) grants (hallitus@prodeko.org)"
            ),
        ),
        (
            "AL",
            "puheenjohtaja@prodeko.org",
            _(
                "Alumni, department and stakeholder relations (puheenjohtaja@prodeko.org)"
            ),
        ),
        (
            "YH",
            "ulkoministeri@prodeko.org",
            _("Cooperation with fellow guilds (ulkoministeri@prodeko.org)"),
        ),
        (
            "AB",
            "abivastaava@prodeko.org",
            _(
                "Marketing to high school students and questions relating applying (abivastaava@prodeko.org)"
            ),
        ),
        (
            "FK",
            "fuksikapteeni@prodeko.org",
            _(
                "New students, freshmen events and education (fuksikapteeni@prodeko.org)"
            ),
        ),
        (
            "MA",
            "maisterikvkapteeni@prodeko.org",
            _("Master and exchange students (maisterikvkapteeni@prodeko.org)"),
        ),
        (
            "ME",
            "mediakeisari@prodeko.org",
            _("Communications, email lists and brand (mediakeisari@prodeko.org)"),
        ),
        ("TI", "cto@prodeko.org", _("IT related questions (cto@prodeko.org)")),
        ("OP", "opintovastaava@prodeko.org", "Studies (opintovastaava@prodeko.org)"),
        (
            "YR",
            "yrityssuhdevastaava@prodeko.org",
            _("Corporate Relations (yrityssuhdevastaava@prodeko.org)"),
        ),
        ("EX", "excumestari@prodeko.org", _("Excursions (excumestari@prodeko.org)")),
        ("TA", "sisakumi@prodeko.org", _("Student events (sisakumi@prodeko.org)")),
        (
            "LA",
            "rahastonhoitaja@prodeko.org",
            _("Billing and finances (rahastonhoitaja@prodeko.org)"),
        ),
        ("ES", "ulkoministeri@prodeko.org", _("ESTIEM (ulkoministeri@prodeko.org)")),
        ("IS", "isovastaava@prodeko.org", _("Tutoring (isovastaava@prodeko.org)")),
    ]
    CONTACT_EMAIL_OPTIONS = []
    for key, value, label in CONTACT_EMAILS:
        CONTACT_EMAIL_OPTIONS.append((key, value))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    email = models.EmailField(blank=True, verbose_name=_("Email"))
    contact_emails = models.CharField(
        blank=False,
        max_length=150,
        choices=CONTACT_EMAIL_OPTIONS,
        verbose_name=_("Who do you wish to contact?"),
    )
    message = models.TextField(blank=False, verbose_name=_("Your message"))
    has_accepted_policies = models.BooleanField(
        blank=True,
        default=False,
        verbose_name=_(
            "I accept that my email address is stored in order to be contacted regarding my message."
        ),
    )

    def __str__(self):
        return f"{self.email} - {self.created_at}"

    class Meta:
        # Correct spelling in Django admin
        verbose_name = _("contact form application")
        verbose_name_plural = _("Contact form")
