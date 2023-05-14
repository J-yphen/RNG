from rng.settings import UPLOAD_PATH, DIR_PATH, ENC_DIR_PATH
from .num_generator import dataQueue
from Crypto.Cipher import AES
import binascii
import os

def makeDir(path_name):
    if not os.path.exists(path_name):
        os.mkdir(path_name)

def encrypt_file(key, in_filename, randomObj, chunksize=64*1024):

    file_name = in_filename.split('.')[0]
    out_filename = ENC_DIR_PATH + file_name + ".enc"
    in_filename = DIR_PATH + in_filename
    
    iv = os.urandom(16)

    encryptor = AES.new(key, AES.MODE_CBC, iv)

    if not os.path.isfile(out_filename):
        mode = "wb"
    else:
        mode = "ab"

    with open(in_filename, 'rb') as infile:
        with open(out_filename, mode) as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    padding = b' ' * (16 - len(chunk) % 16)
                    chunk = chunk + padding

                enc_chunk = encryptor.encrypt(chunk)
                outfile.write(binascii.hexlify(enc_chunk))

def entry():
    makeDir(UPLOAD_PATH)
    makeDir(DIR_PATH)
    makeDir(ENC_DIR_PATH)
    try:
        files = os.listdir(DIR_PATH)
        random_Obj = dataQueue()
        key = bytes(os.urandom(16))
        for file in files:
            encrypt_file(key, file, random_Obj)

        for file in files:
            os.remove(DIR_PATH+file)
    except Exception as e:
        print(e)
        pass