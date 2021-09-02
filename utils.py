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


def nextOperation(success, current_opertion):
    # if transaction a success
    if success:
        # if bught crypto switch to selling in next loop
        if current_opertion:
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
        if current_opertion:
            message = ['Could NOT BUY crypto']
            is_next_operation_buy = True
        # try to sell again in next loop since it failed to sell
        else:
            message = ['Could NOT SELL crypto']
            is_next_operation_buy = False

            log_message('WARNING', message)

    return is_next_operation_buy
