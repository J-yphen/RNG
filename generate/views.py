from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from threading import Thread
import json
import uuid
import time
import os
import datetime
from dateutil.relativedelta import relativedelta
from .models import Token
from .forms import MyForm
from rng.settings import UPLOAD_PATH, DIR_PATH, ENC_DIR_PATH
from .num_generator import dataQueue

randNumObj = dataQueue()

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
        t = Thread(target=writeFile, args=[file])
        t.run()
        try:
            obj = Token.objects.get(token=token)
        except:
            #token invalid -> return error / bad rng
            error = {
            "error" : "Token Not Found",
            "status" : "201",
            "message" : "Invalid token or token expired"
            }
            return JsonResponse(error)
        # todo: add file size to obj.data and save
        obj.data += len(file)*8
        obj.save()
        if num_bits > obj.data:
            #not enough uploaded data -> return error  / bad rng
            error = {
            "error" : "",
            "status" : "201",
            "message" : "Invalid token or token expired"
            }
            return JsonResponse(error)
        #todo: return true rng
        randNum = randNumObj.generator(num_bits)
        data = {"rnum" : randNum}
        obj.data -= num_bits
        obj.save()
        #todo: Check return code
        return JsonResponse(data)
    except Exception as e:
        print(e)
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
    temp_token.save()
    return JsonResponse(vla)

def makeDir(path_name):
    if not os.path.exists(path_name):
        os.mkdir(path_name)

def form(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            #return the key by  rendering same page or diff ans
            print("Correct key")
            pass
        else:
            #return/render form.html with a message
            print("invalid form")
    else:
        form = MyForm()
    return render(request, 'form.html', {'form': form})

def writeFile(data):
    if data == "":
        return
    makeDir(UPLOAD_PATH)
    makeDir(DIR_PATH)
    makeDir(ENC_DIR_PATH)

    file_name = time.strftime("%Y%m%d-%H%M%S%p")
    file_path = DIR_PATH + file_name + ".dat"

    mode = ""

    if not os.path.isfile(file_path):
        mode = "wb"
    else:
        mode = "ab"

    with open(file_path, mode) as f:
        f.write(data.encode())
    
