from rng.settings import ENC_DIR_PATH
import queue
import sys
import os

maxSize = 20971520 # 20 MB
# blockSize = 8192 # 1KB
blockSize = 4
numQueue = queue.Queue(maxSize)

def generator():
    fill()
    num = int.from_bytes(numQueue.get(0), byteorder=sys.byteorder)
    print(num)

def fill():
    try:
        files = os.listdir(ENC_DIR_PATH)
    except:
        print("NO FILE EXISTS")
        return
    for file in files:
        file_path = ENC_DIR_PATH + file
        try:
            with open (file_path, "rb") as f:
                data = f.read(blockSize)
                numQueue.put(data)
                f.seek(blockSize+1)
                # print(data)
                # numQueue.put()
        except:
            print("blaaa")
            pass
        
        break