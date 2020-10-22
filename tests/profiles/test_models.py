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

@pytest.mark.django_db
def test_profile_followers(predef_db_setup):

	user_j = User.objects.get(username='john')
	user_m = User.objects.get(username='monkey')
	profile_j = user_j.profile

	profile_j.followers.add(user_m)

	assert user_m.following.first() == user_j.profile
	assert profile_j.followers.count() == user_m.following.count() 
