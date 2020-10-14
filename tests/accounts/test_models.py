import pytest

from django.contrib.auth import get_user_model, login, logout

User = get_user_model()

@pytest.mark.django_db
def test_register_user():
	#Given
	payload = { 'username': 'Tão', 'password': 'test'}

	#When
	user = User.objects.create_user(payload['username'], payload['password'])
	
	#Then
	assert User.objects.all().count() == 1
	assert User.objects.filter(username=payload['username']).get() == user
