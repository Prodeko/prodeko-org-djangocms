"""The membership status screen.

An account gets its matrikkeli profile the first time it signs in, and
that profile carries no membership date until someone pays or an admin
fills one in, so ``member_until`` is NULL for every fresh account.
"""

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


def _member(member_until, email="member@prodeko.org"):
    """A logged-in account whose profile has the given membership date."""
    user = User.objects.create_user(email=email)
    person = user.person
    person.member_until = member_until
    person.save()
    return user


def test_a_profile_without_a_membership_date_renders(client):
    user = _member(None)
    client.force_login(user)

    response = client.get(reverse("alumnirekisteri:membership_status"))

    assert response.status_code == 200
    assert response.context["has_membership_date"] is False
    assert response.context["should_pay"] is False
    assert response.context["is_expired"] is False


def test_an_unknown_membership_date_is_not_reported_as_paid(client):
    user = _member(None)
    client.force_login(user)

    response = client.get(reverse("alumnirekisteri:membership_status"))

    content = response.content.decode()
    assert "membership status is unknown" in content
    assert "You have paid your membership fee" not in content
    assert "Your membership has expired" not in content


def test_a_membership_ending_soon_offers_the_payment_button(client):
    user = _member(date.today() + timedelta(days=30))
    client.force_login(user)

    response = client.get(reverse("alumnirekisteri:membership_status"))

    assert response.context["has_membership_date"] is True
    assert response.context["should_pay"] is True
    assert response.context["is_expired"] is False
    assert "stripe-buy-button" in response.content.decode()


def test_a_membership_far_in_the_future_is_reported_as_paid(client):
    user = _member(date.today() + timedelta(days=365))
    client.force_login(user)

    response = client.get(reverse("alumnirekisteri:membership_status"))

    assert response.context["has_membership_date"] is True
    assert response.context["should_pay"] is False
    assert response.context["is_expired"] is False
    assert "You have paid your membership fee" in response.content.decode()


def test_a_membership_in_the_past_is_reported_as_expired(client):
    user = _member(date.today() - timedelta(days=1))
    client.force_login(user)

    response = client.get(reverse("alumnirekisteri:membership_status"))

    assert response.context["has_membership_date"] is True
    assert response.context["should_pay"] is False
    assert response.context["is_expired"] is True
    assert "Your membership has expired" in response.content.decode()
