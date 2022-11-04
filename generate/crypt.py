from cryptography.fernet import Fernet
from subprocess import Popen
import binascii
import base64
import mmap
import os


dir_path = os.path.dirname(__file__) + '\\..\\Uploads\\Temp\\'
key = base64.urlsafe_b64encode(b'00000000000000000000000000000000')
large =  False
MAX = 12000

def encryptBlock(m):
    f = Fernet(key)
    if large:
        while m.tell() != m.size():
            if m.size() - m.tell() < MAX:
                block = m.read(m.size() - m.tell())
            else:
                block = m.read(MAX)
            random_data = binascii.hexlify(f.encrypt(block))
            file_handler = os.path.dirname(__file__) + "\\file_handler.py"
            Popen(["python", file_handler, random_data, ".enc", file])
            m.seek(MAX+1)
    
    data = m.read(m.size())
    random_data = binascii.hexlify(f.encrypt(data))
    file_handler = os.path.dirname(__file__) + "\\file_handler.py"
    Popen(["python", file_handler, random_data, ".enc", file])


files = os.listdir(dir_path)
for file in files:
    f = open(dir_path+file, 'r+b')
    m = mmap.mmap(f.fileno(), 0)
    size = m.size()
    if size > MAX:
        large = True
    else:
        large = False
    
    data = m.read(size)
    f.close()
    encryptBlock(m)