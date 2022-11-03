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
    json_data = json.loads(request.body)
    try:
        file = json_data["file"]
        token = json_data["token"]
        num_bits = json_data["size"]
        data = {"rnum" : "0"}
        return JsonResponse(data)
    except:
        error = {
            "error" : "Invalid JSON Request",
            "status" : "201",
            "message" : "file, token or size field not found"
            }
        return JsonResponse(error)