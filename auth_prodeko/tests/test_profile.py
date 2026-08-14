import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture(autouse=True)
def _db(db):
    pass


def test_profile_form_has_no_password_fields():
    from auth_prodeko.forms import EditProfileForm

    assert set(EditProfileForm().fields) == {"email"}


def test_profile_page_lets_a_user_change_their_email(client):
    user = User.objects.create_user(email="before@prodeko.org")
    client.force_login(user)
    response = client.post("/en/profile/", {"email": "after@prodeko.org"})
    assert response.status_code == 302
    user.refresh_from_db()
    assert user.email == "after@prodeko.org"


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
