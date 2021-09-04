import os
from datetime import date, timedelta, datetime
import pandas as pd


class PriceHistory():
    def __init__(self, directory='price_history'):
        self.file_path = ''
        self.__directory = directory
        self.filePath()
        self.__data = dict()

    def historyDirectory(self):
        current_dir = PriceHistory.getCurrentDirectory()
        history_dir = os.path.join(current_dir, self.__directory)
        if not os.path.isdir(history_dir):
            os.mkdir(history_dir)
        return history_dir

    def filePath(self):
        file_name = '.'.join(['market', 'csv'])
        history_directory = self.historyDirectory()
        self.file_path = os.path.join(history_directory, file_name)

    def appendData(self):
        if not os.path.isfile(self.file_path):
            df = pd.DataFrame(data=self.__data)
            df.to_csv(self.file_path, index=False)
        else:
            df = pd.read_csv(self.file_path)
            new_data = pd.DataFrame(data=self.__data)
            df = df.append(new_data, ignore_index=True)
            df.to_csv(self.file_path, index=False)

    def setData(self, bid, ask):
        self.__data['date time'] = [PriceHistory.getDateTime()]
        self.__data['bid'] = bid
        self.__data['ask'] = ask

    @staticmethod
    def getCurrentDirectory():
        return os.path.dirname(os.path.realpath(__file__))

    @staticmethod
    def getDate():
        today = date.today()
        return today.strftime("%Y-%m-%d")

    @staticmethod
    def getDateTime():
        now = datetime.today()
        return now.strftime("%Y-%m-%d %H:%M:%S")
