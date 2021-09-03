from datetime import date, timedelta, datetime
import pandas as pd
import os

# missing to update today and yesterday path


class TradeHistory:
    def __init__(self, directory='data'):
        self.today_path = ''
        self.yesterday_path = ''
        self.__data = dict()
        self.__directory = directory

        self.todayPath()
        self.yesterdayPath()

    def historyDirectory(self):
        current_dir = TradeHistory.getCurrentDirectory()
        history_dir = os.path.join(current_dir, self.__directory)
        if not os.path.isdir(history_dir):
            os.mkdir(history_dir)
        return history_dir

    def todayPath(self):
        today = TradeHistory.getDate()
        file_name = '.'.join([today, 'csv'])
        history_directory = self.historyDirectory()
        self.today_path = os.path.join(history_directory, file_name)

    def yesterdayPath(self):
        today = TradeHistory.getYesterday()
        file_name = '.'.join([today, 'csv'])
        history_directory = self.historyDirectory()
        self.yesterday_path = os.path.join(history_directory, file_name)

    def csvPath(self):
        self.todayPath()
        self.yesterdayPath()
        if os.path.isfile(self.today_path):
            return self.today_path
        elif os.path.isfile(self.yesterday_path):
            return self.yesterday_path
        elif os.listdir(self.historyDirectory()):
            files = os.listdir(self.historyDirectory())
            files = [file for file in files if file.endswith('.csv')]
            if files:
                files.sort()
                path = os.path.join(self.historyDirectory(), files[-1])
                return path
            else:
                return ''

    def appendData(self):
        self.todayPath()
        self.yesterdayPath()
        if not os.path.isfile(self.today_path):
            df = pd.DataFrame(data=self.__data)
            df.to_csv(self.today_path, index=False)
        else:
            df = pd.read_csv(self.today_path)
            new_data = pd.DataFrame(data=self.__data)
            df = df.append(new_data, ignore_index=True)
            df.to_csv(self.today_path, index=False)
        # store new data in variable for further reference
        # self.__data = data

    def getData(self):
        # if corrects data already stored
        if 'date time' in self.__data and TradeHistory.getDate() in self.__data['date time']:
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

    def setData(self, success: str, transaction: bool, assets, amount, price, amount_received, percentage):
        '''
        Creates dictionary with necessary data
        '''

        self.__data['date time'] = [TradeHistory.getDateTime()]
        self.__data['success'] = [success]
        self.__data['assets'] = [assets]
        if not success:
            self.__data['transaction'] = ['ERROR']
        elif transaction:
            self.__data['transaction'] = ['BUY']
        elif not transaction:
            self.__data['transaction'] = ['SELL']
        self.__data['price'] = [price]
        self.__data['amount'] = [amount]
        self.__data['obtained'] = [amount_received]
        self.__data['percentage'] = [percentage]

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
