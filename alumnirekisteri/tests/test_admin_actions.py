import pytest
from django.contrib.auth import get_user_model
from django.urls import NoReverseMatch, reverse

User = get_user_model()


@pytest.fixture(autouse=True)
def _db(db):
    pass


@pytest.fixture
def staff_client(client):
    user = User.objects.create_user(
        email="admin@prodeko.org", is_staff=True, is_active=True
    )
    client.force_login(user)
    return client


def test_pending_requests_screen_is_gone():
    with pytest.raises(NoReverseMatch):
        reverse("alumnirekisteri:admin_member_requests")


def test_privilege_actions_are_rejected(staff_client):
    """Anything these set would be overwritten at the next login."""
    victim = User.objects.create_user(email="victim@prodeko.org")
    response = staff_client.post(
        reverse("alumnirekisteri:admin"),
        {"action": "make-admin", "user_id": victim.pk},
    )
    assert response.status_code == 403
    victim.refresh_from_db()
    assert victim.is_staff is False


def test_admin_notes_still_work(staff_client):
    victim = User.objects.create_user(email="victim@prodeko.org")
    staff_client.post(
        reverse("alumnirekisteri:admin"),
        {"admin_note": "Maksanut", "user_id": victim.pk},
    )
    victim.refresh_from_db()
    assert victim.person.admin_note == "Maksanut"
