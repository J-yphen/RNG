from apscheduler.schedulers.background import BackgroundScheduler
from generate import crypt
from generate import fast_crypt
from generate.views import delete_expired
        
def start():
	scheduler = BackgroundScheduler()
	# scheduler.add_job(crypt.entry, 'interval', weeks=1)
	# scheduler.add_job(crypt.entry, 'interval', minutes=1)
	scheduler.add_job(fast_crypt.entry, 'interval', minutes=1)
	scheduler.add_job(delete_expired, 'interval', weeks=6)
	scheduler.start()