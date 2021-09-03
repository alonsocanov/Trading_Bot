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


def operationToBool(current_opertion):
    if isinstance(current_opertion, str):
        if current_opertion == 'BUY':
            current_opertion = True
        else:
            current_opertion = False
    return current_opertion


def nextOperation(success, current_opertion):
    current_opertion = operationToBool(current_opertion)
    # if transaction a success
    if success:
        # if bught crypto switch to selling in next loop
        if current_opertion:
            is_next_operation_buy = False
        # if sold crypto switch to buying in next loop
        else:
            is_next_operation_buy = True
    # if error in transaction
    else:
        # try to buy again in next loop since it failed to buy
        if current_opertion:
            is_next_operation_buy = True
        # try to sell again in next loop since it failed to sell
        else:
            is_next_operation_buy = False

    return is_next_operation_buy
