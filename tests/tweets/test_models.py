import pytest
from tweets.models import Tweet
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_tweet_model(predef_db_setup):
	user = User.objects.get(username="john")
	tweet = Tweet(content="This is a test tweet omg nsfw thanks!", user=user)
	tweet.save()
	assert tweet.content == "This is a test tweet omg nsfw thanks!"
	# assert tweet.created_date
	# assert tweet.updated_date
	assert "This is a test tweet omg nsfw thanks!" == tweet.content

	assert user == tweet.user


@pytest.mark.django_db
def test_tweet_descending_ordering():
	user = User.objects.create(username="carl")

	tweet = Tweet(content="This is a test tweet omg nsfw thanks!", user=user)
	tweet.save()
	tweet2 = Tweet(content="Je ne sais pas", user=user)
	tweet2.save()
	tweet3 = Tweet(content="Alo galera do kaô", user=user)
	tweet3.save()

	tweets = Tweet.objects.all()
	# print(tweets)
	assert len(tweets) == 3
	assert [tweet for tweet in tweets] == [tweet3, tweet2, tweet]


@pytest.mark.django_db
def test_likes(predef_db_setup):
	# Given
	user_j = User.objects.get(username='john')
	user_m = User.objects.get(username='monkey')
	tweet_j = Tweet.objects.filter(user=user_j).first()
	assert tweet_j.content != '' 
	assert tweet_j.likes.exists() == False
	assert tweet_j.likes.count() == 0

	# When
	tweet_j.likes.add(user_m)

	# Then
	assert tweet_j.content != ''
	assert tweet_j.likes.count() == 1
	assert tweet_j.likes.exists() == True
	assert tweet_j.likes.first() == user_m

@pytest.mark.django_db
def test_likes_remove(predef_db_setup):
	user_j = User.objects.get(username='john')
	user_m = User.objects.get(username='monkey')
	tweet_j = Tweet.objects.filter(user=user_j).first()
	assert tweet_j.content != '' 
	assert tweet_j.likes.exists() == False
	assert tweet_j.likes.count() == 0

	tweet_j.likes.add(user_m)
	assert tweet_j.likes.first() == user_m
	tweet_j.likes.remove(user_m)

	assert tweet_j.likes.first() == None
	assert tweet_j.likes.exists() == False

@pytest.mark.django_db
def test_likes_more_than_once(predef_db_setup):
	user_j = User.objects.get(username='john')
	user_m = User.objects.get(username='monkey')
	tweet_j = Tweet.objects.filter(user=user_j).first()
	assert tweet_j.content != '' 
	assert tweet_j.likes.exists() == False
	assert tweet_j.likes.count() == 0

	tweet_j.likes.add(user_m)
	tweet_j.likes.add(user_m)

	assert tweet_j.likes.count() == 1

@pytest.mark.django_db
def test_retweet(predef_db_setup):

	user_j = User.objects.get(username='john')
	user_m = User.objects.get(username='monkey')
	tweet_j = Tweet.objects.filter(user=user_j).first()

	tweet_m = Tweet.objects.create(user=user_m, parent=tweet_j)

	assert tweet_m.is_retweet == True
	assert tweet_m.parent == tweet_j


@pytest.mark.django_db
def test_related_names(predef_db_setup):

	user_j = User.objects.get(username='john')
	user_m = User.objects.get(username='monkey')
	tweet_j = Tweet.objects.filter(user=user_j).first()
	assert tweet_j.content != '' 
	assert tweet_j.likes.exists() == False
	assert tweet_j.likes.count() == 0

	tweet_j.likes.add(user_m)
	
	assert user_m.tweet_user.all().count() == user_m.tweetlike_set.all().count() # likes
	assert user_j.tweets.all().count() == Tweet.objects.filter(user=user_j).count()
	assert user_j.tweets.first() == tweet_j

