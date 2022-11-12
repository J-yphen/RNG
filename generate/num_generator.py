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
        except:
            print("NO FILE EXISTS")
            return

        for file in files:
            file_path = ENC_DIR_PATH + file
            try:
                with open (file_path, "rb") as f:
                    while True:
                        data = f.read(self.blockSize)
                        if not data:
                            break
                        self.numQueue.put(data)
            except:
                pass
            
            if self.numQueue.full():
                break
            
            self.renameFile(file)
    
    def generator(self, num_bits):
        if self.numQueue.empty():
            self.fill()
        num = self.numQueue.get(0)
        print(int(num.decode(), 16))
        num = int(num.decode(), 16)
        return num

    def renameFile(self, file):
        os.rename(ENC_DIR_PATH + file, DIR_PATH + file.split('.')[0] + ".dat" )