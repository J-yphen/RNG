from cryptography.fernet import Fernet
import binascii
import base64
import mmap
import os


uploads_path = os.path.dirname(__file__) + '\\..\\Uploads\\'
dir_path = os.path.dirname(__file__) + '\\..\\Uploads\\Temp\\'
enc_dir_path = os.path.dirname(__file__) + '\\..\\Uploads\\Encrypted\\'

key = base64.urlsafe_b64encode(b'00000000000000000000000000000000')

def makeDir(path_name):
    if not os.path.exists(path_name):
        os.mkdir(path_name)

def storeFile(data, file):
    makeDir(uploads_path)
    makeDir(dir_path)
    makeDir(enc_dir_path)

    file_name = file.split('.')[0]
    file_path = enc_dir_path + file_name + ".enc"
    mode = ""

    if not os.path.isfile(file_path):
        mode = "wb"
    else:
        mode = "ab"

    with open(file_path, mode) as f:
        f.write(data)
    

def encryptBlock(m, file):
    f = Fernet(key)
    data = m.read(m.size())
    random_data = binascii.hexlify(f.encrypt(data))
    storeFile(random_data, file)


def entry():
    files = os.listdir(dir_path)
    for file in files:
        f = open(dir_path+file, 'r+b')
        m = mmap.mmap(f.fileno(), 0)
        f.close()
        encryptBlock(m, file)

    for file in files:
        try:
            os.remove(dir_path+file)
        except:
            pass