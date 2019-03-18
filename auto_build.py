#coding:utf8
#pip3 install schedule
import schedule
import time
import auto

def job():
    auto.clean_all()
    auto.pull_all()
    auto.build_all()
    auto.dput_all()


schedule.every().day.at("12:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(10)
