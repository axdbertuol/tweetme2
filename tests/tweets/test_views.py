import json
import pytest

from tweets.models import Tweet
from tweets.views import tweet_create_view

# decorator > permission to access db
@pytest.mark.django_db
def test_add_tweet(client):
    tweets = Tweet.objects.all()
    assert len(tweets) == 0

    tweets.create(content="This is a test tweet")
    response = client.get(
        "/tweets/1", 
        content_type="application/json"
    )

    assert response.status_code == 200

    tweets = Tweet.objects.all()
    assert len(tweets) == 1

@pytest.mark.django_db
def test_create_tweet(client):

    tweets = Tweet.objects.all()
    
    response = client.post(
        '/create-tweet',
        {
            "content": "This is a test tweet"
        }
    )

    assert response.status_code == 200
    assert len(tweets) == 1
    assert tweets.get(id=1).content == "This is a test tweet"

    
