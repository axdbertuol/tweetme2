import pytest

from django.contrib.auth import get_user_model
from profiles.models import Profile
from tweets.models import Tweet

User = get_user_model()


@pytest.mark.django_db
def test_profile_showing(predef_db_setup, client):
    user = User.objects.get(username="monkey")
    # Given
    client.force_login(user)
    # When
    response = client.get("/profile/monkey")

    assert response.status_code == 200
