from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from threading import Thread
import json
import uuid
import time
import os

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
    return JsonResponse(vla)

def makeDir(path_name):
    if not os.path.exists(path_name):
        os.mkdir(path_name)

def writeFile(data):
    uploads_path = os.path.dirname(__file__) + '\\..\\Uploads\\'
    dir_path = os.path.dirname(__file__) + '\\..\\Uploads\\Temp\\'
    enc_dir_path = os.path.dirname(__file__) + '\\..\\Uploads\\Encrypted\\'
    makeDir(uploads_path)
    makeDir(dir_path)
    makeDir(enc_dir_path)

    file_name = time.strftime("%Y%m%d-%H%M%S%p")
    file_path = dir_path + file_name + type

    mode = ""

    if not os.path.isfile(file_path):
        mode = "wb"
    else:
        mode = "ab"

    with open(file_path, mode) as f:
        f.write(data.encode())