from datetime import date, timedelta, datetime
import pandas as pd
import os


class CsvHistory:
    def __init__(self, directory='data'):
        self.today_path = ''
        self.yesterday_path = ''
        self.__data = dict()
        self.__directory = directory

    def historyDirectory(self):
        current_dir = CsvHistory.getCurrentDirectory()
        history_dir = os.path.join(current_dir, self.__directory)
        if not os.path.isdir(history_dir):
            os.mkdir(history_dir)
        return history_dir

    def todayPath(self):
        today = CsvHistory.getDate()
        file_name = '.'.join([today, 'csv'])
        history_directory = self.historyDirectory()
        self.today_path = os.path.join(history_directory, file_name)

    def yesterdayPath(self):
        today = CsvHistory.getYesterday()
        file_name = '.'.join([today, 'csv'])
        history_directory = self.historyDirectory()
        self.today_path = os.path.join(history_directory, file_name)

    def csvPath(self):
        if os.path.isfile(self.today_path):
            return self.today_path
        elif os.path.isfile(self.yesterday_path):
            return self.yesterday_path
        else:
            return None

    def createCsv(self, data: dict()):
        if not os.path.isfile(self.today_path):
            df = pd.DataFrame(data=data)
            df.to_csv(self.today_path, index=False)
            self.__data = data

    def append(self, data: dict()):
        if not os.path.isfile(self.today_path):
            df = pd.DataFrame(data=data)
            df.to_csv(self.today_path, index=False)
        else:
            df = pd.read_csv(self.today_path)
            new_data = pd.DataFrame(data=data)
            df = df.append(new_data, ignore_index=True)
            df.to_csv(self.today_path, index=False)

        self.__data = data

    def getData(self):
        # if corrects data already stored
        if 'date time' in self.__data and CsvHistory.getDate() in self.__data['date time']:
            return self.__data
        else:
            file_path = self.csvPath()
            if file_path:
                df = pd.read_csv(file_path)
                data = df.tail(1).to_dict('list')
                for key in list(data.keys()):
                    if isinstance(data[key], list):
                        self.__data[key] = data[key][-1]
        return self.__data

    @staticmethod
    def getDate():
        today = date.today()
        return today.strftime("%Y-%m-%d")

    @staticmethod
    def getYesterday():
        today = date.today()
        yesterday = today - timedelta(days=1)
        return yesterday.strftime("%Y-%m-%d")

    @staticmethod
    def getDateTime():
        now = datetime.today()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def getCurrentDirectory():
        return os.path.dirname(os.path.realpath(__file__))
