import json
import pytest

from tweets.models import Tweet
from tweets.views import tweet_create_view
from django.contrib.auth import get_user_model

User = get_user_model()

# decorator > permission to access db

@pytest.mark.django_db
def test_create_tweet(client):

    tweets = Tweet.objects.all()
    user = User.objects.create(username='carl')
    response = client.post("/create-tweet", {"content": "This is a test tweet", "user": user})

    assert response.status_code == 200
    assert len(tweets) == 1
    assert tweets.get(id=1).content == "This is a test tweet"


@pytest.mark.django_db
def test_tweet_error_too_long(client):

    toolong = ''
    for _ in range(300):
        toolong += 'a'
    user = User.objects.create(username='carl')
    response = client.post("/create-tweet", {"content": toolong, "user": user}, content_type='application/json')
    tweets = Tweet.objects.all()

    print(response.content)
    assert response.status_code == 400
    assert len(tweets) == 0

    


