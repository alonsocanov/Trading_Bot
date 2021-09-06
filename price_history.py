from math import gamma
import os
from datetime import date, timedelta, datetime
from numpy.lib.function_base import gradient
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
        self.__data['date time'] = [pd.to_datetime(PriceHistory.getDateTime())]
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

    def getLastEntry(self):
        df = pd.read_csv(self.file_path)
        data = df.tail(1).to_dict('list')
        return data

    def getData(self, num_days: int = None):
        df = pd.read_csv(self.file_path)
        if num_days:
            start_date = PriceHistory.getLastNDay(num_days)
            data = df[pd.to_datetime(df['date time'])
                      > pd.to_datetime(start_date)]
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

    def gradient(self, num_days: int = None, plot: bool = False):
        title = 'BTC Prices'
        df = self.getData(num_days)
        start_date = pd.to_datetime(df['date time'].iloc[0])
        df['date time'] = pd.to_datetime(df['date time'])
        sec_difference = (df['date time'] - start_date).dt.total_seconds()
        df['sec_from_start'] = sec_difference

        x_plot = [df['date time'].values[0], df['date time'].values[-1]]

        x_pred = [[df['sec_from_start'].values[0]],
                  [df['sec_from_start'].values[-1]]]
        model = PriceHistory.priceFit(df['sec_from_start'], df['bid'])
        y_hat = model.predict(x_pred)

        if plot:
            x_label = 'Date Time'
            y_label = 'Price'

            plt.figure(figsize=(16, 5), dpi=100)
            plt.scatter(df['date time'], df['bid'], color='tab:red')
            plt.plot(x_plot, y_hat, color='red')
            plt.gca().set(title=title, xlabel=x_label, ylabel=y_label)
            plt.show()

        gradient = (y_hat[-1] - y_hat[0]) / \
            (df['sec_from_start'].values[-1] - df['sec_from_start'].values[0])
        return gradient
