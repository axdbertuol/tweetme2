from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import Tweet

def home_view(request):
    # return HttpResponse("<h1>Hello World</h1>")
    return render(request, "pages/home.html")

def tweet_detail_view(request, tweet_id):
    """
        Return JSON data for JavaScript
    """
    data = {
        "id": tweet_id,
    }
    status = 200 # OK status
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = 'Not Found'
        status = 404
        return JsonResponse(data=data, status=status)

    return JsonResponse(data=data, status=status)

def tweet_list_view(request, *args, **kwargs):
    queryset = Tweet.objects.all()
    tweets_list = [{"id": x.id, "content": x.content} for x in queryset]

    data = {
        "response": tweets_list
    }

    return JsonResponse(data=data)
