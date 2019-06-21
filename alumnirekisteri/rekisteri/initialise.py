# Use this model to create initial data during development

from auth2.models import User
from rekisteri.models import Person


def create_admin_profile(
    email="admin@admin.fi", password="salasana", first_name="Admin", last_name="Admin"
):
    """ creates an admin profile with the given credentials """
    if not User.objects.filter(email=email).count() == 0:
        return False
    admin = User.objects.create_superuser(email, password)
    admin.first_name = first_name
    admin.last_name = last_name
    admin.save()
    person, created = Person.objects.get_or_create(user=admin)
    if not created:
        return False
    return person
