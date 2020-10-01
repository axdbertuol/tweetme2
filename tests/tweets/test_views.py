import json
import pytest

from tweets.models import Tweet
from tweets.views import tweet_create_view
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
    assert response.status_code == 201
    assert len(tweets) == 1
    print(Tweet.objects.all().values_list())
    assert tweets.get(user=user, id=1).content == "This is a test tweet"


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

    


