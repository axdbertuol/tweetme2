import random
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.http import is_safe_url
from rest_framework.response import Response
from rest_framework.decorators import (
	api_view,
	permission_classes,
	authentication_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .models import Tweet
from .forms import TweetForm
from .serializers import TweetSerializer, TweetActionSerializer, TweetCreateSerializer

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request):
	# return HttpResponse("<h1>Hello World</h1>")
	return render(request, "pages/feed.html")

def tweets_list_view(request):
	return render(request, "tweets/list.html")

def tweets_detail_view(request, tweet_id):
	return render(request, "tweets/detail.html", context={"tweetId": tweet_id})

# def tweets_profile_view(request, username):
# 	return render(request, "tweets/profile.html", context={"profile_username": username})


def tweet_create_view_pure_django(request):
	user = request.user
	if not user.is_authenticated:
		user = None
		if request.is_ajax():
			return JsonResponse({}, status=401)  # unauthorized
		return redirect(settings.LOGIN_URL)
	form = TweetForm(request.POST or None)
	next_url = request.POST.get("next") or None
	if form.is_valid():
		obj = form.save(commit=False)
		obj.user = user
		obj.save()
		if request.is_ajax():
			# 201 == created items
			return JsonResponse(obj.serialize(), status=201)
		if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
			return redirect(next_url)
		form = TweetForm()
	elif form.errors or form.non_field_errors:
		if request.is_ajax():
			return JsonResponse(form.errors, status=400)
		else:
			print("passi")
			return HttpResponse(form.errors, status=400)
	return render(request, "components/form.html", context={"form": form})


def tweet_detail_view_pure_django(request, tweet_id):
	"""
	Return JSON data for JavaScript
	"""
	data = {
		"id": tweet_id,
	}
	status = 200  # OK status
	try:
		obj = Tweet.objects.get(id=tweet_id)
		data["content"] = obj.content
	except:
		data["message"] = "Not Found"
		status = 404
		return JsonResponse(data=data, status=status)

	return JsonResponse(data=data, status=status)


def tweet_list_view_pure_django(request, *args, **kwargs):
	queryset = Tweet.objects.all()
	tweets_list = [x.serialize() for x in queryset]

	data = {"response": tweets_list}

	return JsonResponse(data=data)
