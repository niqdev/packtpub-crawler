from apscheduler.schedulers.blocking import BlockingScheduler
import os
import shutil

sched = BlockingScheduler()

#@sched.scheduled_job('cron', hour=11)

@sched.scheduled_job('interval', minutes=2)
def scheduled_job():
    print(os.listdir(os.curdir))
    shutil.rmtree('./ebooks', ignore_errors=True)
    print(os.listdir(os.curdir))

    print('New job: packtpub-crawler')
    os.system('python script/spider.py --config config/prod.cfg --upload drive --notify')

sched.start()
