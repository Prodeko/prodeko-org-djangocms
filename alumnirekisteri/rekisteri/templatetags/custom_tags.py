from urllib.parse import unquote, urlencode

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context["request"].GET.dict()
    query.update(kwargs)
    return urlencode(query)


def latex_escape(value):
    return mark_safe(
        value.replace("&", "§§&")
        .replace("#", "§§#")
        .replace("_", "§§_")
        .replace("\\", "§§textbackslash ")
        .replace("§§", "\\")
    )


latex_escape.is_safe = True


def get_image_filename(value):
    return mark_safe(unquote(value.split("/")[-1]))


get_image_filename.is_safe = True


def test_empty(value):
    return value and value != " "


def sortByEndDate(x):
    return -(
        (x.end_year if x.end_year else 10000 + (x.start_year if x.start_year else 0))
        * 12
        + (x.end_month if hasattr(x, "end_month") and x.end_month else 0)
    )


def sortByYear(x):
    return -(x.year if x.year else 0)


def sortedByEndDate(x):
    return sorted(x, key=sortByEndDate)


def sortedByYear(x):
    return sorted(x, key=sortByYear)


def person_is_empty(person):
    return not (
        person.birthdate
        or person.address
        or person.postal_code
        or person.city
        or person.gender
        or person.marital_status
        or person.military_rank
        or person.class_of_year
        or person.phones.all()
        or person.educations.all()
        or person.work_experiences.all()
        or person.positions_of_trust.all()
        or person.student_organizational_activities.all()
        or person.volunteers.all()
        or person.honors.all()
        or person.interests.all()
        or person.languages.all()
        or person.languages.all()
        or person.get_family_members_sorted()
    )


def person_category(person):
    if person.member_type == 5:
        return "kunniajäsenet"
    elif person.is_tuta_doctor():
        return "tohtorit"
    elif person.is_tuta_lisensiaatti():
        return "lisensiaatit"
    return "alumni"


register.filter("latex_escape", latex_escape)
register.filter("test_empty", test_empty)
register.filter("get_image_filename", get_image_filename)
register.filter("sortedByEndDate", sortedByEndDate)
register.filter("sortedByYear", sortedByYear)
register.filter("person_is_empty", person_is_empty)
register.filter("person_category", person_category)
