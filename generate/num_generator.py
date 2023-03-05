from rng.settings import ENC_DIR_PATH, DIR_PATH
import queue
import os

class dataQueue:
    maxSize = 20971520*2 # 20 MB
    blockSize = 8 # 4 BYTES
    numQueue = queue.Queue(maxSize)

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
                    while True:
                        data = f.read(self.blockSize)
                        if not data or len(data) < self.blockSize:
                            break
                        self.numQueue.put(data)
            except:
                pass
            
            if self.numQueue.full():
                break
            
            self.renameFile(file)
    
    def generator(self, num_bytes):
        if self.numQueue.empty():
            self.fill()

        try:
            num = self.numQueue.get(0)
            num = num[:(num_bytes%(32))] # 32 = 8 * 4 because 4 bytes
            for block in range(num_bytes//(32)):
                num += self.numQueue.get(0)
            # print(int(num.decode(), 16))
            num = int(num.decode(), 16)
            
        except Exception as e:
            print(f"\033[1;31;40m[!] Empty Stream: \033[0m{e}")
        
        return num

    def renameFile(self, file):
        try:
            os.rename(ENC_DIR_PATH + file, DIR_PATH + file.split('.')[0] + ".dat")
        except:
            os.replace(ENC_DIR_PATH + file, DIR_PATH + file.split('.')[0] + ".dat")