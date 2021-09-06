import os
from datetime import date, timedelta, datetime
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model


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

    @staticmethod
    def getLastNDay(num_days):
        date = datetime.today() - timedelta(num_days)
        return date.strftime("%Y-%m-%d %H:%M:%S")

    def trend(self, num_days=5):
        pass

    def getData(self, num_days: int = None):
        df = pd.read_csv(self.file_path)
        if num_days:
            data = df.tail(num_days).to_dict('list')
        else:
            data = df
        return data

    @staticmethod
    def priceFit(x, y):
        x = x.values.reshape(-1, 1)
        y = y.values
        model = linear_model.LinearRegression().fit(x, y)
        linear_model.LinearRegression(
            copy_X=True, fit_intercept=True, n_jobs=1, normalize=False)

        return model

    def plot(self, num_days: int = None):
        title = 'BTC Prices'
        df = self.getData(num_days)
        x = pd.to_datetime(df['date time'])
        y = df['ask']

        if not num_days:
            start_date = x[0]
        else:
            start_date = PriceHistory.getLastNDay(num_days)

        # x_pred = [[x.values[0]], [x.values[-1]]]

        # model = PriceHistory.priceFit(x, y)
        # y_hat = model.predict(x_pred)

        x_label = 'Date Time'
        y_label = 'Price'

        plt.figure(figsize=(16, 5), dpi=100)
        plt.scatter(x, y, color='tab:red')
        # plt.plot(x_pred, y_hat, color='blue')
        plt.gca().set(title=title, xlabel=x_label, ylabel=y_label)
        plt.show()
