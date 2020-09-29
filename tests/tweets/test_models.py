import pytest
from tweets.models import Tweet
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_tweet_model():
    user = User.objects.create(username='carl')
    tweet = Tweet(content="This is a test tweet omg nsfw thanks!", user=user)
    tweet.save()
    assert tweet.content == "This is a test tweet omg nsfw thanks!"
    # assert tweet.created_date
    # assert tweet.updated_date
    assert str(tweet) == tweet.content
    assert user == tweet.user
@pytest.mark.django_db
def test_tweet_descending_ordering():
    user = User.objects.create(username='carl')

    tweet = Tweet(content="This is a test tweet omg nsfw thanks!", user=user)
    tweet.save()
    tweet2 = Tweet(content="Je ne sais pas", user=user)
    tweet2.save()
    tweet3 = Tweet(content="Alo galera do kaô", user=user)
    tweet3.save()

    tweets = Tweet.objects.all()
    # print(tweets)
    assert len(tweets) == 3
    assert [ tweet for tweet in tweets ] == [ tweet3, tweet2, tweet ]

@pytest.mark.django_db
def test_tweet_user_fake_db(db_setup):
    # print(tweets)
    assert len(Tweet.objects.all()) == 25