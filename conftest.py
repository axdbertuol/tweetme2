import pytest
import random
from faker import Faker
from tweets.models import Tweet
from django.contrib.auth import get_user_model

User = get_user_model()


def faker_seed():
    # fake = Faker()
    return random.randint(0, 10000)


@pytest.fixture
@pytest.mark.django_db
def db_setup(request, faker):

    
    users = make_users(faker)
    content_arr = make_tweet_contents(faker)

 
    for c in content_arr:
        Tweet.objects.create(content=c, user=users[random.randint(0,8)])
    
    def fin():
        yield [tweet for tweet in Tweet.objects.all()]
    



@pytest.mark.django_db
def make_users(faker):

    users = []

    for i in range(0, 9):
        username = faker.profile(fields="username")["username"]
        users.append(User.objects.get_or_create(username=username)[0])

    return users


def make_tweet_contents(faker, nb_texts=25, max_nb_chars=240):
    return faker.texts(nb_texts=nb_texts, max_nb_chars=max_nb_chars)
