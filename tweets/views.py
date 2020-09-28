import random
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.http import is_safe_url

from .models import Tweet
from .forms import TweetForm

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request):
    # return HttpResponse("<h1>Hello World</h1>")
    return render(request, "pages/home.html")


def tweet_create_view(request):
    form = TweetForm(request.POST or None)
    print('ajax', request.is_ajax())
    next_url = request.POST.get("next") or None
    print(next_url)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201) # 201 == created items
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, "components/form.html", context={"form": form})


def tweet_detail_view(request, tweet_id):
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


def tweet_list_view(request, *args, **kwargs):
    queryset = Tweet.objects.all()
    tweets_list = [x.serialize() for x in queryset]

    data = {"response": tweets_list}

    return JsonResponse(data=data)
