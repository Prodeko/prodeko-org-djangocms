def test_user_fixture_creates_member(user):
    assert user.pk is not None
    assert user.email == "fixture-user@prodeko.org"


def test_logged_in_client_is_authenticated(logged_in_client):
    assert "_auth_user_id" in logged_in_client.session
