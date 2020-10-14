import json
import pytest

from tweets.models import Tweet
# from tweets.api.views import tweet_create_view
from django.contrib.auth import get_user_model

User = get_user_model()

# decorator > permission to access db

@pytest.mark.django_db
def test_create_tweet(client):

	user = User.objects.create(username='carl')
	client.force_login(user)
	response = client.post(
		"/api/tweets/create", 
		{"content": "This is a test tweet"},
		content_type= "application/json"
	)

	tweets = Tweet.objects.all()
	data = response.json()
	assert response.status_code == 201
	assert len(tweets) == 1
	assert data.get("content") == "This is a test tweet"

@pytest.mark.django_db
def test_tweet_error_too_long(client):

	toolong = ''
	for _ in range(300):
		toolong += 'a'
	user = User.objects.create(username='carl')
	client.force_login(user)

	response = client.post("/api/tweets/create", {"content": toolong}, content_type='application/json')
	tweets = Tweet.objects.all()
	assert response.data['content'][0] == 'This tweet is too long'
	assert response.status_code == 400
	assert len(tweets) == 0

	


@pytest.mark.django_db
def test_delete_tweet(client):

	user = User.objects.create(username='carl')
	client.force_login(user)
	tweet = Tweet.objects.create(content='alo', user=user)
	assert Tweet.objects.all().count() == 1

	response = client.post(f"/api/tweets/{tweet.id}/delete", content_type="application/json")

	assert response.status_code == 200
	assert Tweet.objects.all().count() == 0

@pytest.mark.django_db
def test_delete_tweet_no_auth(client):

	user = User.objects.create(username='carl')
	tweet = Tweet.objects.create(content='alo', user=user)
	assert Tweet.objects.all().count() == 1

	response = client.post(f"/api/tweets/{tweet.id}/delete", content_type="application/json")

	assert response.status_code == 403 # forbidden
	assert Tweet.objects.all().count() == 1

@pytest.mark.django_db
def test_delete_non_exist_tweet(client):

	user = User.objects.create(username='carl')
	client.force_login(user)
	Tweet.objects.create(content='alo', user=user)
	assert Tweet.objects.all().count() == 1

	response = client.post("/api/tweets/2/delete", content_type="application/json")

	assert response.status_code == 404

@pytest.mark.django_db
def test_delete_tweet_from_other(client):

	user = User.objects.create(username='carl')
	user2 = User.objects.create(username='dax')
	tweet = Tweet.objects.create(content='alo', user=user)
	client.force_login(user2)
	assert Tweet.objects.all().count() == 1

	response = client.post(f"/api/tweets/{tweet.id}/delete", content_type="application/json")

	assert response.status_code == 401

@pytest.mark.django_db
def test_action_like_tweet(client):
	user = User.objects.create(username='carl')
	user2 = User.objects.create(username='dax')
	tweet = Tweet.objects.create(content='alo', user=user)
	client.force_login(user2)

	response = client.post("/api/tweets/action", {"id": tweet.id, "action": "like"}, content_type="application/json")

	assert response.status_code == 200
	assert response.data["content"] == "alo"
	assert tweet.likes.count() == 1
	assert user.tweetlike_set.count() == user.tweet_user.count()

@pytest.mark.django_db
def test_action_unlike_tweet(client):
	user = User.objects.create(username='carl')
	user2 = User.objects.create(username='dax')
	tweet = Tweet.objects.create(content='alo', user=user)
	client.force_login(user2)

	response = client.post("/api/tweets/action", {"id": tweet.id, "action": "like"}, content_type="application/json")
	assert response.status_code == 200
	assert tweet.likes.count() == 1

	response = client.post("/api/tweets/action", {"id": tweet.id, "action": "unlike"}, content_type="application/json")
	assert response.status_code == 200
	assert tweet.likes.count() == 0

@pytest.mark.django_db
def test_action_retweet(client):

	user = User.objects.create(username='carl')
	user2 = User.objects.create(username='dax')
	tweet = Tweet.objects.create(content='alo', user=user)
	client.force_login(user2)

	response = client.post("/api/tweets/action", {"id": tweet.id, "action": "retweet"}, content_type="application/json")

	data = response.json()
	assert response.status_code == 201
	assert tweet.id != data.get("id")