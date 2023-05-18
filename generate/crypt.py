from cryptography.fernet import Fernet
from rng.settings import UPLOAD_PATH, DIR_PATH, ENC_DIR_PATH
import binascii
import mmap
import os

key = Fernet.generate_key()

def makeDir(path_name):
    if not os.path.exists(path_name):
        os.mkdir(path_name)

def storeFile(data, file):
    makeDir(UPLOAD_PATH)
    makeDir(DIR_PATH)
    makeDir(ENC_DIR_PATH)

    file_name = file.split('.')[0]
    file_path = ENC_DIR_PATH + file_name + ".enc"
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
    storeFile(random_data[65:], file)


def entry():
    try:
        files = os.listdir(DIR_PATH)
        for file in files:
            f = open(DIR_PATH+file, 'r+b')
            m = mmap.mmap(f.fileno(), 0)
            f.close()
            encryptBlock(m, file)
            m.close()

        for file in files:
            os.remove(DIR_PATH+file)
    except:
        pass