from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
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

@csrf_exempt
@require_POST
def upload(request):
    json_data = json.loads(request.body)
    try:
        file = json_data["file"]
        token = json_data["token"]
        t = Thread(target=writeFile, args=[file])
        t.run()
        try:
            obj = Token.objects.get(token=token)
        except:
            #token invalid -> return error / bad rng
            error = {
            "error" : "Token Not Found",
            "status" : "400",
            "message" : "Invalid token or token expired"
            }
            return JsonResponse(error)
        # add file size to obj.data, increases time and saves
        obj.data += len(file)*8
        obj.exp =  datetime.date.today() + relativedelta(months=3)
        obj.save()
        success = {
            "status" : "200",
            "message" : "File successfully uploaded."
            }
        return JsonResponse(success)
    except Exception as e:
        print(e)
        error = {
            "error" : "Invalid JSON Request",
            "status" : "400",
            "message" : "file, token or size field not found"
            }
        return JsonResponse(error)

@csrf_exempt
@require_POST
def generate(request):
    json_data = json.loads(request.body)
    try:
        token = json_data["token"]
        num_bytes = json_data["size"]
        try:
            obj = Token.objects.get(token=token)
        except:
            #token invalid -> return error / bad rng
            error = {
            "error" : "Token Not Found",
            "status" : "400",
            "message" : "Invalid token or token expired"
            }
            return JsonResponse(error)
        if num_bytes > obj.data:
            # not enough uploaded data -> return error
            error = {
            "error" : "Data Insufficient",
            "status" : "400",
            "message" : "Required size of random number too large"
            }
            return JsonResponse(error)
        # return rng
        randNum = randNumObj.generator(num_bytes*2)
        data = {"rnum" : randNum}
        obj.data -= num_bytes
        obj.save()
        return JsonResponse(data)
    except Exception as e:
        print(e)
        error = {
            "error" : "Invalid JSON Request",
            "status" : "400",
            "message" : "file, token or size field not found"
            }
        return JsonResponse(error)

def keygen():
    api_token = uuid.uuid4()
    dt = datetime.date.today() + relativedelta(months=3)
    temp_token = Token(token=api_token, data=0, exp=dt)
    temp_token.save()
    return api_token

def makeDir(path_name):
    if not os.path.exists(path_name):
        os.mkdir(path_name)

def form(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            #return the key by rendering same page
            message = "Key: " + str(keygen())
        else:
            #return form.html with error message
            # message = "Captcha Error"
            message = ""
    else:
        form = MyForm()
        message=''
    return render(request, 'generate/index.html', {'form': form, 'message': message})

def delete_expired():
    now = datetime.date.today()
    Token.objects.filter(exp__lt = now).delete()

try:
    delete_expired()
    randNumObj.fill()
except:
    print("[!] Failed to delete expired token.")
    pass

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
    

@csrf_exempt
@require_POST
def user_quota(request):
    json_data = json.loads(request.body)
    try:
        token = json_data["token"]
        try:
            obj = Token.objects.get(token=token)
        except:
            #token invalid -> return error / bad rng
            error = {
            "error" : "Token Not Found",
            "status" : "400",
            "message" : "Invalid token or token expired"
            }
            return JsonResponse(error)        
        data = {
            "remaining": obj.data,
            "validity": obj.exp
        }

        # Return remaining data that a user can use and it's token validity
        return JsonResponse(data)
    except Exception as e:
        print(e)
        error = {
            "error" : "Invalid JSON Request",
            "status" : "400",
            "message" : "file, token or size field not found"
            }
        return JsonResponse(error)