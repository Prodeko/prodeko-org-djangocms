from cms.api import create_page
from cms.constants import TEMPLATE_INHERITANCE_MAGIC
from django.test import RequestFactory, TestCase

from prodekoorg.views import handler500


class MissingApphookPageTest(TestCase):
    """The site must keep serving even when no apphook pages exist.

    The footer links to the contact apphook. That URL namespace is only
    registered while a published CMS page has the apphook attached, and
    an admin can unpublish or delete such a page at any time. Rendering
    must degrade to hiding the link instead of raising NoReverseMatch on
    every request.
    """

    @classmethod
    def setUpTestData(cls):
        # A regular page without any apphook: the DB state after an admin
        # has deleted the apphook pages.
        cls.home = create_page(
            title="etusivu",
            template=TEMPLATE_INHERITANCE_MAGIC,
            language="fi",
            published=True,
        )

    def test_page_renders_without_apphook_pages(self):
        response = self.client.get(self.home.get_absolute_url("fi"))
        self.assertEqual(response.status_code, 200)

    def test_404_page_renders_without_apphook_pages(self):
        response = self.client.get("/fi/does-not-exist/")
        self.assertEqual(response.status_code, 404)


class FooterApphookLinkTest(TestCase):
    """The footer must show the apphook link whenever its page exists."""

    @classmethod
    def setUpTestData(cls):
        cls.home = create_page(
            title="etusivu",
            template=TEMPLATE_INHERITANCE_MAGIC,
            language="fi",
            published=True,
        )
        cls.contact = create_page(
            title="ota yhteyttä",
            template=TEMPLATE_INHERITANCE_MAGIC,
            language="fi",
            published=True,
            apphook="ContactApphook",
            apphook_namespace="app_contact",
        )

    def test_footer_contains_apphook_link(self):
        response = self.client.get(self.home.get_absolute_url("fi"))
        self.assertContains(response, self.contact.get_absolute_url("fi"))


class Handler500Test(TestCase):
    """500.html must render with a bare request and an empty database.

    The 500 handler runs when anything else has already failed, so its
    template cannot depend on middleware state, CMS pages or URL
    namespaces.
    """

    def test_500_page_renders_with_bare_request(self):
        request = RequestFactory().get("/fi/")
        response = handler500(request)
        self.assertEqual(response.status_code, 500)
