from rng.settings import ENC_DIR_PATH, DIR_PATH
import os

class dataQueue:
    maxSize = 20971520*2 # 20 MB
    r, w = os.pipe() # creates a pipe which resides in memory
    currSize = 0

    def __init__(self):
        pass

    def fill(self):
        try:
            files = os.listdir(ENC_DIR_PATH)
        except Exception as e:
            print(f"\033[1;31;40m[!] File not exists: \033[0m{e}")
            return

        for file in files:
            file_path = ENC_DIR_PATH + file
            try:
                with open (file_path, "rb") as f:
                    self.currSize += os.write(self.w, f.read()) # os.write(w, b) returns num of bytes which is added to current size
            except:
                pass
            self.renameFile(file)
            if self.currSize > self.maxSize: # exit condition
                break
    
    def generator(self, num_bytes):
        if self.currSize <= num_bytes: # fill if not availaible. Note: use offset and multiprocessing if possible, we can pass writing file descripter and it should work using os.fork(). Issue: updating currSize
            self.fill()
        try:
            self.currSize -= num_bytes 
            num = os.read(self.r, num_bytes)
            num = int(num.decode(), 16)
            
        except Exception as e:
            print(f"\033[1;31;40m[!] Empty Stream: \033[0m{e}")
        
        return num

    def renameFile(self, file):
        try:
            os.rename(ENC_DIR_PATH + file, DIR_PATH + file.split('.')[0] + ".dat")
        except:
            os.replace(ENC_DIR_PATH + file, DIR_PATH + file.split('.')[0] + ".dat")