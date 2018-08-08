import logging
import time
from logging.handlers import TimedRotatingFileHandler

def logger():
    day = time.strftime("%Y-%m-%d",time.localtime())
    log = logging.getLogger(__name__)
    log.setLevel(level = logging.DEBUG)
    logfile = TimedRotatingFileHandler('log.txt','D',1,0)
    logfile.setLevel(logging.INFO)
    screen = logging.StreamHandler()
    screen.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s -%(lineno)d - %(levelname)s - %(message)s')
    logfile.setFormatter(formatter)
    log.addHandler(logfile)
    log.addHandler(screen)
    return log
if __name__=='__main__':
    pass