from datetime import datetime
import os

from apscheduler.schedulers.background import BackgroundScheduler
from generate import crypt
        
def start():
        scheduler = BackgroundScheduler()
        scheduler.add_job(crypt.entry, 'interval', weeks=1)
        scheduler.start()