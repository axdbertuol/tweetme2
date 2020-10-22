import pytest

from django.contrib.auth import get_user_model
from profiles.models import Profile
from tweets.models import Tweet

User = get_user_model()


@pytest.mark.django_db
def test_profile_showing(predef_db_setup, client):
    # Given
    user = User.objects.get(username="monkey")
    client.force_login(user)
    # When
    response = client.get("/profile/monkey")

    assert response.status_code == 200

@pytest.mark.django_db
def test_profile_follow(predef_db_setup, client):
	user_m = User.objects.get(username="monkey")
	user_j = User.objects.get(username='john')
	client.force_login(user_m)

	response = client.post(
		"/api/profile/john/follow", 
		{"action": "follow"}, 
		content_type="application/json"
	)

	data = response.json()
	assert response.status_code == 200
	assert data.get("count") == 1
	assert user_j.profile.followers.first() == user_m

@pytest.mark.django_db
def test_profile_unfollow(predef_db_setup, client):
	user_m = User.objects.get(username="monkey")
	user_j = User.objects.get(username='john')
	client.force_login(user_m)

	response = client.post(
		"/api/profile/john/follow", 
		{"action": "follow"}, 
		content_type="application/json"
	)
	assert response.status_code == 200
	assert user_j.profile.followers.first() == user_m
	response = client.post(
		"/api/profile/john/follow", 
		{"action": "unfollow"}, 
		content_type="application/json"
	)
	
	data = response.json()
	assert response.status_code == 200
	assert data.get("count") == 0
	assert user_j.profile.followers.first() == None

@pytest.mark.django_db
def test_profile_cannot_follow_self(predef_db_setup, client):
	user_m = User.objects.get(username="monkey")
	client.force_login(user_m)

	response = client.post(
		"/api/profile/monkey/follow", 
		{"action": "follow"}, 
		content_type="application/json"
	)
	data = response.json()
	assert response.status_code == 400
	assert data.get("count") == None
	assert user_m.profile.followers.first() == None