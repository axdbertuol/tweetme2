import random
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.utils.http import is_safe_url
from rest_framework.response import Response
from rest_framework.decorators import (
	api_view,
	permission_classes,
	authentication_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from profiles.models import Profile
from profiles.serializers import PublicProfileSerializer
ALLOWED_HOSTS = settings.ALLOWED_HOSTS

User = get_user_model()

# @api_view(["GET", "POST"])  # http method == POST
# @authentication_classes([SessionAuthentication])
# @permission_classes([IsAuthenticated])
# def user_follow_view(request, username):
# 	current_user = request.user
# 	other_user_qs = User.objects.filter(username=username)
# 	if not other_user_qs.exists():
# 		return Response({}, status=404)
# 	elif current_user == other_user_qs.first():
# 		return Response({}, status=400)
# 	other_user_profile = other_user_qs.first().profile
# 	data = request.data or {}
# 	action = data.get('action')
	
# 	if action == 'unfollow':
# 		other_user_profile.followers.remove(current_user)
# 	elif action == 'follow':
# 		other_user_profile.followers.add(current_user)
# 	# current_followers_qs = other_user_profile.followers.all()
# 	data = PublicProfileSerializer(instance=other_user_profile, context={"request": request})
# 	return Response(data.data, status=200)

@api_view(["GET", "POST"]) 
def profile_detail_api_view(request, username):
	#get the profile for the passed username
	current_user = request.user
	other_user_qs = Profile.objects.filter(user__username=username)
	if not other_user_qs.exists():
		return Response({"detail": "User not found"}, status=404)
	profile_obj = other_user_qs.first()
	data = request.data or {}
	if request.method == 'POST':
		action = data.get('action')
		if current_user != profile_obj.user:
			if action == 'unfollow':
				profile_obj.followers.remove(current_user)
			elif action == 'follow':
				profile_obj.followers.add(current_user)
			else:
				pass
		else:
			return Response({"detail": "Cannot follow self."}, status=400)

	serializer = PublicProfileSerializer(instance=profile_obj, context={"request": request})
	return Response(serializer.data, status=200)

