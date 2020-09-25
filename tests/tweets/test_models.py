import pytest
from tweets.models import Tweet

@pytest.mark.django_db
def test_tweet_model():
    tweet = Tweet(content="This is a test tweet omg nsfw thanks!")
    tweet.save()
    assert tweet.content == "This is a test tweet omg nsfw thanks!"
    # assert tweet.created_date
    # assert tweet.updated_date
    assert str(tweet) == tweet.content
