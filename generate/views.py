from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
# from .models import Poll

def upload(request):
    data = {"msg" : "hello!"}
    return JsonResponse(data)
    # MAX_OBJECTS = 20
    # polls = Poll.objects.all()[:MAX_OBJECTS]
    # data = {"results": list(polls.values("question", "created_by__username", "pub_date"))}
    # return JsonResponse(data)


@csrf_exempt
@require_POST
def generate(request):
    # if request.method == "POST":
    data = {"msg" : "hello!"}
    json_data = json.loads(str(request.body, encoding='utf-8'))
    print(json_data)
    return JsonResponse(data)
    # poll = get_object_or_404(Poll, pk=pk)
    # data = {"results": {
    #     "question": poll.question,
    #     "created_by": poll.created_by.username,
    #     "pub_date": poll.pub_date
    # }}
    # return JsonResponse(data)
