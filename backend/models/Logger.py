import logging
import time
from logging.handlers import RotatingFileHandler
from datetime import datetime

# class that manage log of the backend application
class Logger:
    def __init__(self, app):
        self.app = app

        log_formatter = logging.Formatter("[%(levelname)s] - %(message)s")
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        logger.addHandler(console_handler)

        max_length_handler = RotatingFileHandler(filename="record.log", mode='a', maxBytes=10*1024*1024, backupCount=2, encoding=None, delay=0)
        max_length_handler.setFormatter(log_formatter)
        logger.addHandler(max_length_handler)

    # info log function
    def info(self, msg, source = ' SERVER  '):
        now = datetime.now()
        self.app.logger.info(f'{source} - - [{now.strftime("%d/%b/%Y %H:%M:%S")}] {msg}')

    # warning log function
    def warning(self, msg, source = ' SERVER  '):
        now = datetime.now()
        self.app.logger.warning(f'{source} - - [{now.strftime("%d/%b/%Y %H:%M:%S")}] {msg}')

    # function for register performance of action and log result
    def performance(self, msg, func, *args):
        bf = self.current_time_ms()
        res = func(*args)
        af = self.current_time_ms()
        self.app.logger.info(f'PERFORMANCE - {msg}: {af-bf} ms')
        return res
    
    # function for get current time in ms
    def current_time_ms(self):
        return round(time.time() * 1000)