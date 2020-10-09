from django.contrib.auth import get_user_model
from rest_framework import authentication

User = get_user_model()

class DevAuthentication(authentication.BasicAuthentication):
	def authenticate(self, request):
		queryset = User.objects.filter(id=1)
		user = queryset.order_by("?").first() # get random user
		return (user, None)