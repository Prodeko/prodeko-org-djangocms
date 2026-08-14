"""Self-service profile deletion in matrikkeli.

Passwords are unusable now that Keycloak owns authentication, so the
confirmation modal identifies the member by their email address instead.
"""

from django.contrib.auth import get_user_model
from django.urls import reverse

from alumnirekisteri.rekisteri.models import Person

User = get_user_model()


def _member(email="member@prodeko.org"):
    """A post_save signal on User creates the matching Person."""
    user = User.objects.create_user(email=email)
    assert Person.objects.filter(user=user).exists()
    return user


def test_confirming_with_your_own_email_deletes_the_profile(client):
    user = _member()
    client.force_login(user)

    response = client.post(
        reverse("alumnirekisteri:delete_profile"), {"username": "member@prodeko.org"}
    )

    assert response.json() == {"success": True}
    assert not User.objects.filter(pk=user.pk).exists()
    assert not Person.objects.exists()


def test_confirming_with_your_own_email_ignores_case(client):
    user = _member()
    client.force_login(user)

    response = client.post(
        reverse("alumnirekisteri:delete_profile"), {"username": "Member@Prodeko.org"}
    )

    assert response.json() == {"success": True}
    assert not User.objects.filter(pk=user.pk).exists()


def test_a_wrong_address_deletes_nothing(client):
    user = _member()
    client.force_login(user)

    response = client.post(
        reverse("alumnirekisteri:delete_profile"), {"username": "someone@prodeko.org"}
    )

    payload = response.json()
    assert payload["success"] is False
    assert payload["errors"]["username"]
    assert User.objects.filter(pk=user.pk).exists()
    assert Person.objects.filter(user=user).exists()


def test_anonymous_requests_are_redirected_to_login(client):
    response = client.post(
        reverse("alumnirekisteri:delete_profile"), {"username": "member@prodeko.org"}
    )

    assert response.status_code == 302
    assert "/login/" in response["Location"]


def test_the_modal_renders_without_a_password_field(client):
    user = _member()
    client.force_login(user)

    response = client.get(reverse("alumnirekisteri:delete_profile"))

    assert response.status_code == 200
    assert set(response.context["form"].fields) == {"username"}
