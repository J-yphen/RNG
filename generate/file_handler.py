import sys
import os
import time

def makeDir(path_name):
    if not os.path.exists(path_name):
        os.mkdir(path_name)


uploads_path = os.path.dirname(__file__) + '\\..\\Uploads\\'
dir_path = os.path.dirname(__file__) + '\\..\\Uploads\\Temp\\'
enc_dir_path = os.path.dirname(__file__) + '\\..\\Uploads\\Encrypted\\'
data = sys.argv[1] # Data to write
type = sys.argv[2] # .dat for writing and .enc for encrypted writing

makeDir(uploads_path)
makeDir(dir_path)
makeDir(enc_dir_path)

if type == ".dat":
    file_name = time.strftime("%Y%m%d-%H%M%S%p")
    file_path = dir_path + file_name + type
elif type == ".enc":
    file_name = sys.argv[3].split('.')[0] # If writing in encrypted file then file name
    file_path = enc_dir_path + file_name + type
else:
    exit(1)
    
mode = ""

if not os.path.isfile(file_path):
    mode = "wb"
else:
    mode = "ab"

with open(file_path, mode) as f:
    f.write(data.encode())