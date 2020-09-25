import json
import pytest

from tweets.models import Tweet

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
    print(response.content)
    # assert response.content["content"] == "This is a test tweet"
    # assert tweets.get
    tweets = Tweet.objects.all()
    assert len(tweets) == 1
