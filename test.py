import unittest
from logs import Log
import utils
import api
import trade
from trade_history import TradeHistory
from price_history import PriceHistory


class TestModules(unittest.TestCase):

    def test_log_class(self):
        print('Testing log file')
        log = Log()
        message = ['Hello World']
        log.message('INFO', message)

    def test_api(self):
        print('Testing Bitso API')
        bot = api.Bitso('config/credentials.json')
        mayor_minor = 'btc_mxn'
        print(bot.assets)
        balance = bot.getBalance('mxn')
        print('Available mxn balance:', balance['mxn']['available'])
        bids = bot.getBids(mayor_minor)
        print('Bids:', bids[0])
        asks = bot.getAsks(mayor_minor)
        print('Asks:', asks[0])
        taker_fee = bot.getTakerPercentageFee(mayor_minor)
        print('Taker fee:', taker_fee)
        maker_fee = bot.getMakerPercentageFee(mayor_minor)
        print('Make fee:', maker_fee)
        print()

    def test_trade_conversions(self):
        print('Testing trade methods')
        bot = api.Bitso('config/credentials.json')
        mayor_minor = 'btc_mxn'
        operation_buy = True
        amount = 150.00
        current_prices = bot.getBids(mayor_minor)
        fee = bot.getTakerPercentageFee(mayor_minor)
        total = trade.conversion(operation_buy, amount, current_prices)
        total_fee = trade.tradeWithFee(total, fee)
        print('Operation Buy:', operation_buy)
        print('Amount:', amount)
        print('Current Market price:', current_prices[:2])
        print('Conversion:', total)
        print('Conversion with fee:', total_fee)
        operation_buy = False
        fee = bot.getMakerPercentageFee(mayor_minor)
        amount = total_fee
        current_prices = bot.getAsks(mayor_minor)
        total = trade.conversion(operation_buy, amount, current_prices)
        total_fee = trade.tradeWithFee(total, fee)
        print('Operation Buy:', operation_buy)
        print('Amount:', amount)
        print('Current Market price:', current_prices[:2])
        print('Conversion:', total)
        print('Conversion with fee:', total_fee)
        print()

    def test_percentage_difference(self):
        print('Testing percentage differences')
        prior_total = 1000.00
        current_total = 1001.00
        print('Prior Total:', prior_total)
        print('Current total:', current_total)
        percentage_diff = trade.percentageDifference(
            prior_total, current_total)
        print('Percentage Difference:', percentage_diff)
        print()

    def test_trade_buy_attempt(self):
        print('Test BUY attempt acording to config')
        UPWARD_TREND_THRESHOLD = 3.0
        DIP_THRESHOLD = -1.00
        prior_total = 100.00
        current_total = 102.00
        operation_buy = True
        print('Prior Total:', prior_total)
        print('Current total:', current_total)
        print('Operation Buy:', operation_buy)
        percentage_diff = trade.percentageDifference(
            prior_total, current_total)
        print('Percentage Difference:', percentage_diff)
        limit_threshold = UPWARD_TREND_THRESHOLD
        trend = DIP_THRESHOLD
        action = trade.attemptToMakeTrade(
            operation_buy, percentage_diff, limit_threshold, trend)
        print('BUY action:', action)
        print()

    def test_trade_sell_attempt(self):
        print('Test SELL attempt acording to config')
        PROFIT_THRESHOLD = 2.5
        STOP_LOSS_THRESHOLD = -2.00
        prior_total = 100.00
        current_total = 101.00
        operation_buy = False
        print('Prior Total:', prior_total)
        print('Current total:', current_total)
        print('Operation Buy:', operation_buy)
        percentage_diff = trade.percentageDifference(
            prior_total, current_total)
        print('Percentage Difference:', percentage_diff)
        limit_threshold = PROFIT_THRESHOLD
        trend = STOP_LOSS_THRESHOLD
        action = trade.attemptToMakeTrade(
            operation_buy, percentage_diff, limit_threshold, trend)
        print('SELL action:', action)
        print()


if __name__ == '__main__':
    test_bot = TestModules()
    test_bot.test_log_class()
    test_bot.test_api()
    test_bot.test_trade_conversions()
    test_bot.test_percentage_difference()
    test_bot.test_trade_buy_attempt()
    test_bot.test_trade_sell_attempt()
