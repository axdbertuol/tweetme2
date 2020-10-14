import pytest
from django.http import Http404

from tweets.models import Tweet
from tweets.api.views import (
    tweet_create_view, tweet_delete_view, 
    tweet_list_view, tweet_detail_view, tweet_action_view,
    TweetCreateSerializer, TweetSerializer
)

from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
@pytest.mark.django_db
def auth_user(client):

    user = User.objects.create(username='forreal')
    client.force_login(user)

    return user


@pytest.mark.django_db
def test_create_tweet(client, monkeypatch, auth_user):
    payload = {"content": "hello world"}

    def mock_create(self, payload):
        return "hello world"
    
    monkeypatch.setattr(TweetCreateSerializer, "create", mock_create)
    monkeypatch.setattr(TweetCreateSerializer, "data", payload)

    resp = client.post("/api/tweets/create", payload, content_type="application/json")
    assert resp.status_code == 201
    assert resp.data["content"] == "hello world"

@pytest.mark.django_db
def test_add_tweet_invalid_json(client, auth_user):
    resp = client.post("/api/tweets/create", {"content": ''}, content_type="application/json")
    assert resp.status_code == 400

# @pytest.mark.django_db
# def test_add_tweet_invalid_json_keys(client, auth_user):
#     resp = client.post("/api/tweets/create", {"contrent": 'xx'}, content_type="application/json")
#     assert resp.status_code == 400

# @pytest.mark.django_db
# def test_get_single_tweet_authenticated(client, mocker, auth_user):
#     payload = {"content": "hello"}

#     def mock_filter(self, id):
#     response = client.get('/api/tweets/1')
#     assert response.status_code == 200
#     assert response.data["content"] == "hello"


