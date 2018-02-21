import requests
import os
import sys
import time

SAVE_NAME = 'progress_do_not_remove'
SAVE_PATH = 'videos'
SLEEP = 1

status = 1

def getProgress():
    if(os.path.exists(SAVE_NAME)):
        with open(SAVE_NAME) as f:
            return int(f.read())
    else:
        return 1

def saveProgress(progress):
    with open(SAVE_NAME, 'w') as f:
        f.write(str(progress))

def run(startAt):
    for aid in range(startAt, 99999999):
        global status
        status = aid
        fetch(aid)
        time.sleep(SLEEP)

def fetch(aid):
    r = requests.get('http://api.bilibili.com/archive_stat/stat?aid=%d' % aid)
    code = r.json()['code']
    message = r.json()['message']
    if code == 0:
        with open('%s/%d.json' % (SAVE_PATH, aid), 'wb') as f:
            f.write(r.content)
        log('%d: <OK>' % aid)
    elif code == 40003:
        log('%d: video not exists' % aid)
    else:
        log('[%d] ERROR %d: %s' % (aid, code, message))
        raise Exception()

def log(message):
    print('%s %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), message))

if __name__ == '__main__':
    progress = getProgress()
    log('start at progress: %d' % progress)
    try:
        run(progress)
    except:
        saveProgress(status)