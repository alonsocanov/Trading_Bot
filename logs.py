import logging
import os
from datetime import date


def getDate():
    today = date.today()
    return today.strftime("%Y-%m-%d")


def getCurrentDirectory():
    return os.path.dirname(os.path.realpath(__file__))


def log_message(message_type, message):
    output_message = list()
    if isinstance(message, list):
        for string in message:
            if not isinstance(string, str):
                output_message.append(str(string))
            else:
                output_message.append(string)
        message = ' '.join(output_message)
    elif not isinstance(message, str):
        message = str(message)
    message_type = message_type.upper()
    if message_type == 'INFO':
        logging.info(message)
    elif message_type == 'WARNING':
        logging.warning(message)
    elif message_type == 'ERROR':
        logging.error(message)
    elif message_type == 'DEBUG':
        logging.debug(message)


def createLogFile():
    today = getDate()
    current_dir = getCurrentDirectory()
    log_dir = os.path.join(current_dir, 'logs')
    if os.path.dirname(log_dir):
        file_name = '.'.join([today, 'log'])
        file_path = os.path.join(log_dir, file_name)
        if not os.path.isfile(file_path):
            file = open(file_path, 'x')
            file.close()
        return file_path
    else:
        log_message('ERROR', 'Directory log does not exist')

# A good log example
# [BALANCE] USD Balance = 22.15$
# [BUY] Bought 0.002 BTC for 22.15 USD
# [PRICE] Last Operation Price updated to 11,171.40 (BTC/USD)
# [ERROR] Could not perform SELL operation - Insufficient balance


# if __name__ != '__main__':
# log configuration
level = logging.INFO
log_path = createLogFile()
logging.basicConfig(filename=log_path, format='%(levelname)s - %(asctime)s - %(message)s',
                    datefmt='%m-%d-%Y %H:%M:%S', level=level)
