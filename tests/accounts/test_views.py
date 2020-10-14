import pytest

from django.contrib.auth import get_user_model, login, logout

User = get_user_model()

@pytest.mark.django_db
def test_register_user(client):
	payload = {"username": 'tst', "password1": 'Test12345', "password2": 'Test12345'}
	
	response = client.post('/register', payload, content_type="application/json" )

	assert response.status_code == 301
