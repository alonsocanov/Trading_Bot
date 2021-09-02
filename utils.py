from datetime import date, timedelta, datetime
import json
import pandas as pd
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
    now = datetime.today()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def getCurrentDirectory():
    return os.path.dirname(os.path.realpath(__file__))


def csvPath(file=''):
    dir = 'data'
    today = getDate()
    if file:
        today = file
    current_dir = getCurrentDirectory()
    log_dir = os.path.join(current_dir, dir)
    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)
        message = ['Directory does not exist:', dir]
        log_message('WARNING', message)
    file_name = '.'.join([today, 'csv'])
    file_path = os.path.join(log_dir, file_name)
    return file_path


def createCsvFile(file_path, data):
    df = pd.DataFrame(data=data)
    df.to_csv(file_path, index=False)
    message = ['Creating CSV file:', file_path]
    log_message('INFO', message)


def appendCsvFile(file_path: str, data: dict):
    df = pd.read_csv(file_path)
    new_data = pd.DataFrame(data=data)
    df = df.append(new_data, ignore_index=True)
    df.to_csv(file_path, index=False)
    message = ['Writing to file:', file_path]
    log_message('INFO', message)


def readLastInputCsv():
    file_path = csvPath()
    data = None
    if not os.path.isfile(file_path):
        message = ['Todays CSV file has not being created:', file_path]
        log_message('INFO', message)
        # try to fetch yesterdays data
        yesterday = getYesterday()
        file_path = csvPath(yesterday)
    if os.path.isfile(file_path):
        df = pd.read_csv(file_path)
        data = df.tail(1).to_dict('list')
        # removin lists from dictionary
        for key in list(data.keys()):
            if isinstance(data[key], list):
                data[key] = data[key][0]
    else:
        message = ['CSV File does not exist:', file_path]
        log_message('WARNING', message)

    return data


def cvsFileAppend(data: dict):
    file_path = csvPath()
    # if file has not being created today
    if not os.path.isfile(file_path):
        createCsvFile(file_path, data)
    # only add new data to existing file
    else:
        appendCsvFile(file_path, data)
    return file_path


def dataDict(success, transaction, assets, amount, price, amount_received, percentage):
    '''
    Creates dictionary with necessary data
    '''
    data = dict()
    data['date time'] = [getDateTime()]
    data['success'] = [success]
    data['assets'] = [assets]
    transaction = transaction.upper().strip()
    if not success:
        data['transaction'] = ['ERROR']
    elif transaction == 'BUY':
        data['transaction'] = ['BUY']
    elif transaction == 'SELL':
        data['transaction'] = ['SELL']
    data['price'] = [price]
    data['amount'] = [amount]
    data['obtained'] = [amount_received]
    data['percentage'] = [percentage]
    return data


def saveHistory(success, transaction, assets, amount, price, amount_received, percentage):
    data = dataDict(success, transaction, assets, amount,
                    price, amount_received, percentage)
    cvsFileAppend(data)
    # if transaction a success
    if success:
        # if bught crypto switch to selling in next loop
        if transaction == 'BUY':
            message = ['Bought crypto']
            is_next_operation_buy = False
        # if sold crypto switch to buying in next loop
        else:
            message = ['Sold crypto']
            is_next_operation_buy = True
        log_message('INFO', message)
    # if error in transaction
    else:
        # try to buy again in next loop since it failed to buy
        if transaction == 'BUY':
            message = ['Could NOT BUY crypto']
            is_next_operation_buy = True
        # try to sell again in next loop since it failed to sell
        else:
            message = ['Could NOT SELL crypto']
            is_next_operation_buy = False

            log_message('WARNING', message)
        is_next_operation_buy = True

    return is_next_operation_buy
