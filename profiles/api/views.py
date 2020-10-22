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

@api_view(["GET", "POST"])  # http method == POST
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def user_follow_view(request, username):
	current_user = request.user
	other_user_qs = User.objects.filter(username=username)
	if not other_user_qs.exists():
		return Response({}, status=404)
	elif current_user == other_user_qs.first():
		return Response({}, status=400)
	other_user_profile = other_user_qs.first().profile
	data = request.data or {}
	action = data.get('action')

	if action == 'unfollow':
		other_user_profile.followers.remove(current_user)
	elif action == 'follow':
		other_user_profile.followers.add(current_user)
	
	return Response({"count": other_user_profile.followers.all().count()}, status=200)

@api_view(["GET"]) 
def profile_detail_api_view(request, username):
	#get the profile for the passed username
	qs = Profile.objects.filter(user__username=username)
	if not qs.exists():
		return Response({"detail": "User not found"}, status=404)
	profile_obj = qs.first()
	data = PublicProfileSerializer(instance=profile_obj, context={"request": request})
	return Response(data.data, status=200)

# @api_view(["GET"])
# def tweet_list_view(request, *args, **kwargs):
# 	queryset = Tweet.objects.all()
# 	username = request.GET.get('username')
# 	if username is not None:
# 		queryset = queryset.filter(user__username__iexact=username)

# 	serializer = TweetSerializer(queryset, many=True)
# 	return Response(serializer.data)


# @api_view(["GET"])
# def user_profile_detail_view(request, tweet_id, *args, **kwargs):
# 	queryset = Tweet.objects.filter(id=tweet_id)
# 	if not queryset.exists():
# 		return Response({}, status=404)
# 	obj = queryset.first()
# 	serializer = TweetSerializer(obj)
# 	return Response(serializer.data, status=200)


# @api_view(["DELETE", "POST"])
# @permission_classes([IsAuthenticated])
# def tweet_delete_view(request, tweet_id, *args, **kwargs):
# 	queryset = Tweet.objects.filter(id=tweet_id)
# 	if not queryset.exists():
# 		return Response({}, status=404)
# 	queryset = queryset.filter(user=request.user)
# 	if not queryset.exists():
# 		return Response({"message": "You cannot delete this tweet."}, status=401)
# 	obj = queryset.first()
# 	obj.delete()
# 	return Response({"message": "Tweet deleted."}, status=200)


# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def tweet_action_view(request, *args, **kwargs):
# 	"""
# 	id is required
# 	Action options are: like, unlike, retweet
# 	"""
# 	serializer = TweetActionSerializer(data=request.data)
# 	print(request.data)
# 	if serializer.is_valid(raise_exception=True):
# 		data = serializer.validated_data
# 		tweet_id = data.get("id")
# 		action = data.get("action")
# 		content = data.get("content")
# 		print(data)
# 		queryset = Tweet.objects.filter(id=tweet_id)
# 		if not queryset.exists():
# 			return Response({}, status=404)
# 		obj = queryset.first()
# 		if action == "like":
# 			obj.likes.add(request.user)
# 			serializer = TweetSerializer(obj)
# 			return Response(serializer.data, status=200)
# 		elif action == "unlike":
# 			obj.likes.remove(request.user)
# 			serializer = TweetSerializer(obj)
# 			return Response(serializer.data, status=200)
# 		elif action == "retweet":
# 			parent_obj = obj
# 			new_tweet = Tweet.objects.create(
# 				user=request.user, parent=parent_obj, content=content
# 			)
# 			serializer = TweetSerializer(new_tweet)
# 			return Response(serializer.data, status=201)

# 	return Response({}, status=200)


# def tweet_create_view_pure_django(request):
# 	user = request.user
# 	if not user.is_authenticated:
# 		user = None
# 		if request.is_ajax():
# 			return JsonResponse({}, status=401)  # unauthorized
# 		return redirect(settings.LOGIN_URL)
# 	form = TweetForm(request.POST or None)
# 	next_url = request.POST.get("next") or None
# 	if form.is_valid():
# 		obj = form.save(commit=False)
# 		obj.user = user
# 		obj.save()
# 		if request.is_ajax():
# 			# 201 == created items
# 			return JsonResponse(obj.serialize(), status=201)
# 		if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
# 			return redirect(next_url)
# 		form = TweetForm()
# 	elif form.errors or form.non_field_errors:
# 		if request.is_ajax():
# 			return JsonResponse(form.errors, status=400)
# 		else:
# 			print("passi")
# 			return HttpResponse(form.errors, status=400)
# 	return render(request, "components/form.html", context={"form": form})


# def tweet_detail_view_pure_django(request, tweet_id):
# 	"""
# 	Return JSON data for JavaScript
# 	"""
# 	data = {
# 		"id": tweet_id,
# 	}
# 	status = 200  # OK status
# 	try:
# 		obj = Tweet.objects.get(id=tweet_id)
# 		data["content"] = obj.content
# 	except:
# 		data["message"] = "Not Found"
# 		status = 404
# 		return JsonResponse(data=data, status=status)

# 	return JsonResponse(data=data, status=status)


# def tweet_list_view_pure_django(request, *args, **kwargs):
# 	queryset = Tweet.objects.all()
# 	tweets_list = [x.serialize() for x in queryset]

# 	data = {"response": tweets_list}

# 	return JsonResponse(data=data)
