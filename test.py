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

    def test_trade_attempt(self):
        print('Testing attemps to make trades and percentage differences')
        pass


if __name__ == '__main__':
    test_bot = TestModules()
    test_bot.test_log_class()
    test_bot.test_api()
    test_bot.test_trade_conversions()
    test_bot.test_trade_attempt()
