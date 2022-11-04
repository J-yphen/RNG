from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
import uuid
import datetime
from dateutil.relativedelta import relativedelta
from .models import Token

def upload(request):
    data = {"msg" : "hello!"}
    return JsonResponse(data)

@csrf_exempt
@require_POST
def generate(request):
    json_data = json.loads(request.body)
    try:
        file = json_data["file"]
        token = json_data["token"]
        num_bits = json_data["size"]
        data = {"rnum" : "0"}

        try:
            obj = Token.objects.get(token=token)
        except:
            #token invalid -> return error / bad rng
            pass
        # todo: add file size to obj.data and save
        obj.data += len(file)
        obj.save()
        if num_bits > obj.data:
            #not enough uploaded data -> return error  / bad rng
            pass
        #todo: return true rng
        return JsonResponse(data)
    except:
        error = {
            "error" : "Invalid JSON Request",
            "status" : "201",
            "message" : "file, token or size field not found"
            }
        return JsonResponse(error)

@require_GET
def keygen(request):
    api_token = uuid.uuid4()
    vla = {"token":f"{api_token}"}
    dt = datetime.date.today() + relativedelta(months=3)
    temp_token = Token(token=api_token, data=0, exp=dt)
    return JsonResponse(vla)