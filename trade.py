from logs import log_message
import config
import api
from utils import strToFloat, floatToStr


def tradeWithFee(amount, fee):
    # gives the amount that will be given including the taker or maker fee
    amount = strToFloat(amount)
    fee = strToFloat(fee)

    total = amount - amount * (fee / 100)

    total = floatToStr(total)
    message = ' '.join(['Trade with fee will give:', total])
    log_message('INFO', message)
    return total


def conversion(amount, book_price):
    amount = strToFloat(amount)
    book_price = strToFloat(book_price)
    total = amount / book_price

    total = floatToStr(total)
    message = ' '.join(['Trade will give:', total])
    log_message('INFO', message)
    return total


def tryToBuy(percentage_diff):
    log_message('INFO', 'Trying to BUY')
    message = ' '.join(['Percentage difference:', str(percentage_diff)])
    log_message('INFO', message)
    message = ' '.join(
        ['Upward trend threshold', str(config.UPWARD_TREND_THRESHOLD)])
    log_message('INFO', message)
    message = ' '.join(
        ['Dip threshold', str(config.DIP_THRESHOLD)])
    log_message('INFO', message)
    if percentage_diff >= config.UPWARD_TREND_THRESHOLD or percentage_diff <= config.DIP_THRESHOLD:
        last_operation_price = api.placeBuyOrder()
        is_next_operation_buy = False
    log_message('INFO', 'NOT BUYING')
    return last_operation_price, is_next_operation_buy


def tryToSell(percentage_diff):
    log_message('INFO', 'Trying to SELL')
    message = ' '.join(['Percentage difference:', str(percentage_diff)])
    log_message('INFO', message)
    message = ' '.join(
        ['Profit threshold', str(config.PROFIT_THRESHOLD)])
    log_message('INFO', message)
    message = ' '.join(
        ['Stop loss threshold', str(config.STOP_LOSS_THRESHOLD)])
    log_message('INFO', message)
    if percentage_diff >= config.PROFIT_THRESHOLD or percentage_diff <= config.STOP_LOSS_THRESHOLD:
        last_operation_price = api.placeBuyOrder()
        is_next_operation_buy = True
    return last_operation_price, is_next_operation_buy


def attemptToMakeTrade(last_operation_price, is_next_operation_buy):
    current_price = api.getMarketPrice()
    percentage_diff = (
        current_price - last_operation_price)/last_operation_price*100
    if is_next_operation_buy:
        tryToBuy(percentage_diff)
    else:
        tryToSell(percentage_diff)


def trackBotInvest():
    # get total invested and what not to move
    my_invest = 300
    currency = 'MXN'
    currency_invested_to = ''
    crypto_amount = ''

    pass
