import pytest
from django.contrib.auth import get_user_model
from profiles.models import Profile

User = get_user_model()


@pytest.mark.django_db
def test_profile_creation_signal():
    # Given
    payload = {"username": "Tão", "password": "test"}

    # When
    user = User.objects.create_user(payload["username"], payload["password"])
    # Then

    assert Profile.objects.filter(user__username=payload["username"]).get().user == user
