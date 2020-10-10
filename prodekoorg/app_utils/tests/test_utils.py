import tempfile

from cms.api import create_page
from cms.constants import TEMPLATE_INHERITANCE_MAGIC
from django.conf import settings
from django.test import TestCase, override_settings

# Override settigs to test translations
english = override_settings(LANGUAGE_CODE="en", LANGUAGES=(("en", "English"),))
finnish = override_settings(LANGUAGE_CODE="fi", LANGUAGES=(("fi", "Finnish"),))


class CommonTestData(TestCase):
    """Common test data used across various apphook tests (e.g. app_kulukorvaus.tests.test_data)

    This is needed because in the base template we are reversing urls for
    app_contact, app_kulukorvaus and app_membership. This class sets up pages required for
    those apphooks.

    Args:
        TestCase: https://docs.djangoproject.com/en/3.1/topics/testing/tools/#django.test.TestCase.
    """

    tmp_dir = None

    @classmethod
    def setUpClass(cls):
        cls.tmp_dir = tempfile.TemporaryDirectory(prefix="mediatest")
        settings.MEDIA_ROOT = cls.tmp_dir.name
        super(CommonTestData, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.tmp_dir = None
        super(CommonTestData, cls).tearDownClass()

    @classmethod
    def setUpTestData(cls):
        cls.page1 = create_page(
            title="yhteydenottolomake",
            template=TEMPLATE_INHERITANCE_MAGIC,
            language="fi",
            created_by=cls.test_user2,
            published=True,
            login_required=True,
            apphook="ContactApphook",
            apphook_namespace="app_contact",
        )

        cls.page2 = create_page(
            title="kulukorvauslomake",
            template=TEMPLATE_INHERITANCE_MAGIC,
            language="fi",
            created_by=cls.test_user2,
            published=True,
            login_required=True,
            apphook="KulukorvausApphook",
            apphook_namespace="app_kulukorvaus",
        )

        cls.page3 = create_page(
            title="jäsenhakemuslomake",
            template=TEMPLATE_INHERITANCE_MAGIC,
            language="fi",
            created_by=cls.test_user2,
            published=True,
            login_required=True,
            apphook="ApplyForMembershipApphook",
            apphook_namespace="app_membership",
        )
