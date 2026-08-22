import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture(autouse=True)
def _db(db):
    pass


def test_profile_page_shows_the_signed_in_members_address(client):
    user = User.objects.create_user(email="mine@prodeko.org")
    client.force_login(user)

    response = client.get("/en/profile/")

    assert response.status_code == 200
    assert "mine@prodeko.org" in response.content.decode()


def test_profile_page_requires_login(client):
    response = client.get("/en/profile/")
    assert response.status_code == 302
    assert "/login/" in response["Location"]


def test_profile_page_ignores_a_posted_email(client):
    """Keycloak owns the address; the page offers no way to change it here."""
    user = User.objects.create_user(email="mine@prodeko.org")
    client.force_login(user)

    client.post("/en/profile/", {"email": "someone-else@prodeko.org"})

    user.refresh_from_db()
    assert user.email == "mine@prodeko.org"


def test_accept_policies_requires_login(client):
    """It reads request.user, so anonymous access used to raise."""
    response = client.get("/en/accept_policies/")
    assert response.status_code == 302
    assert "/login/" in response["Location"]


def test_accept_policies_sets_the_flag(client):
    user = User.objects.create_user(email="a@prodeko.org")
    client.force_login(user)
    client.get("/en/accept_policies/")
    user.refresh_from_db()
    assert user.has_accepted_policies is True
