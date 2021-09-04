import logging
import os
from datetime import date


class Log:
    def __init__(self, directory='logs') -> None:
        self.__file_path = ''
        self.__level = logging.INFO
        self.__directory = directory

        self.__format = '%(levelname)s - %(asctime)s - %(message)s'
        self.__datefmt = '%m-%d-%Y %H:%M:%S'

    def config(self):
        self.createLogFile()
        logging.basicConfig(filename=self.__file_path, format=self.__format,
                            datefmt=self.__datefmt, level=self.__level)

    @staticmethod
    def getDate():
        today = date.today()
        return today.strftime("%Y-%m-%d")

    @staticmethod
    def getCurrentDirectory():
        return os.path.dirname(os.path.realpath(__file__))

    def logDirectory(self):
        current_dir = Log.getCurrentDirectory()
        history_dir = os.path.join(current_dir, self.__directory)
        if not os.path.isdir(history_dir):
            os.mkdir(history_dir)
        return history_dir

    def createLogFile(self):
        today = Log.getDate()
        log_dir = self.logDirectory()
        if os.path.dirname(log_dir):
            file_name = '.'.join([today, 'log'])
            file_path = os.path.join(log_dir, file_name)
            if not os.path.isfile(file_path):
                file = open(file_path, 'x')
                file.close()
            self.__file_path = file_path

    def message(self, message_type, message):
        self.config()
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


# A good log example
# [BALANCE] USD Balance = 22.15$
# [BUY] Bought 0.002 BTC for 22.15 USD
# [PRICE] Last Operation Price updated to 11,171.40 (BTC/USD)
# [ERROR] Could not perform SELL operation - Insufficient balance
