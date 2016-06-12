from apscheduler.schedulers.blocking import BlockingScheduler
import os
import shutil

sched = BlockingScheduler()

#@sched.scheduled_job('interval', minutes=5)

@sched.scheduled_job('cron', hour=9)
def scheduled_job():
    print('New job: packtpub-crawler')
    #print(os.listdir(os.curdir))
    shutil.rmtree('./ebooks', ignore_errors=True)
    os.system('python script/spider.py --config config/prod.cfg --upload drive --notify')

sched.start()
