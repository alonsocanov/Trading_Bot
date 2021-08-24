from datetime import date, timedelta
import json
import os
import sys
from logs import log_message
import time


def strToFloat(value: str):
    if not isinstance(value, float):
        value = float(value)
    return value


def floatToStr(value: float):
    if not isinstance(value, str):
        value = str(value)
    return value


def sleep(var: float):
    # ints are equivalent to seconds
    time.sleep(var)


def readJson(file_path: str):
    if os.path.isfile(file_path):
        file = open(file_path)
        data = json.load(file)
        file.close()
        return data
    else:
        message = ['Could find file:', file_path]
        log_message('ERROR', message)
        sys.exit('Error opening file')


def getDate():
    today = date.today()
    return today.strftime("%Y-%m-%d")


def getYesterday():
    today = date.today()
    yesterday = today - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")


def getDateTime():
    now = date.today()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def getCurrentDirectory():
    return os.path.dirname(os.path.realpath(__file__))


def createFile(dir: str, ext: str):
    today = getDate()
    current_dir = getCurrentDirectory()
    log_dir = os.path.join(current_dir, dir)
    if os.path.dirname(log_dir):
        file_name = '.'.join([today, ext.strip('.')])
        file_path = os.path.join(log_dir, file_name)
        if not os.path.isfile(file_path):
            file = open(file_path, 'x')
            file.close()
        return file_path
    else:
        message = ['Directory does not exist:', dir]
        log_message('ERROR', message)
        sys.exit('Could not find directory')


def jsonAppend(file_path: str, data: dict):
    if isinstance(data, dict):
        if os.path.isfile(file_path):
            file = open(file_path, 'a')
            json.dump(data, file)
            file.close()
        else:
            message = ['File does not exist:', file_path]
            log_message('ERROR', message)
            sys.exit('File does not exist')
    else:
        message = ['Variable not a dictionary:', data]
        log_message('ERROR', message)
        sys.exit('Variable not a dictionar')


def jsonData(transaction: str, amount: float or str, price: float or str, percentage: float or str):
    data = dict()
    data['date'] = getDateTime()
    transaction = transaction.upper().strip()
    if transaction == 'BUY':
        data['transaction'] = 'BUY'
    elif transaction == 'SELL':
        data['transaction'] = 'SELL'
    else:
        message = ['Transaction not in options [BUY, SELL]:', transaction]
        log_message('WARNING', message)
    data['price'] = price
    data['amount'] = amount
    data['perrcentage'] = percentage

    return data


def readJson(file_path):
    data = None
    if os.path.isfile(file_path):
        file = open(file_path)
        data = json.load(file)
        file.close()
    else:
        message = ['File does not exist:', file_path]
        log_message('ERROR', message)
    return data


def getPreviousData(data: dict):
    prev_data = None
    # check in history if program stopped
    if not data:
        # check if a file today exists
        today = getDate()
        file_path = 'data/' + today + '.json'
        prev_data = readJson(file_path)
        # if temp data check previous day
        if not prev_data:
            yesterday = getYesterday()
            file_path = 'data/' + yesterday + '.json'
            prev_data = readJson(file_path)
    else:
        prev_data = data
    return prev_data
