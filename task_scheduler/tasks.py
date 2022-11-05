from datetime import datetime
import os

from apscheduler.schedulers.background import BackgroundScheduler
from generate import crypt

# def do_some_thing():
#     f = open("blas.txt", "a")
#     f.write("ewwavbbievbwue")
        
def start():
        scheduler = BackgroundScheduler()
        scheduler.add_job(crypt.entry, 'interval', minutes=1)
        scheduler.start()