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
    message = ['Trade with fee will give:', total]
    log_message('INFO', message)
    return total


def mayorMinorConversion(amount, books: list):
    amount = strToFloat(amount)
    total = 0
    needed = None
    for book in books:
        price = strToFloat(book['price'])
        total += amount / price
        if not needed:
            needed = total
        if strToFloat(book['amount']) < needed:
            needed -= strToFloat(book['amount'])
        else:
            break

    total = floatToStr(total)
    message = ['Trade will give:', total]
    log_message('INFO', message)
    return total


def tryToBuy(percentage_diff, upward_trend_threshold, dip_threshold):
    log_message('INFO', 'Trying to BUY')
    message = ['Percentage difference:', percentage_diff, '%']
    log_message('INFO', message)
    if percentage_diff >= upward_trend_threshold or percentage_diff <= dip_threshold:
        log_message('INFO', 'BUYING')
        last_operation_price = api.placeBuyOrder()
        is_next_operation_buy = False
    return last_operation_price, is_next_operation_buy


def tryToSell(percentage_diff, profit_threshold, stop_loss_threshold):
    log_message('INFO', 'Trying to SELL')
    message = ['Percentage difference:', percentage_diff]
    log_message('INFO', message)
    if percentage_diff >= profit_threshold or percentage_diff <= stop_loss_threshold:
        log_message('INFO', 'SELLING')
        last_operation_price = api.placeSellOrder()
        is_next_operation_buy = True
    return last_operation_price, is_next_operation_buy


def attemptToMakeTrade(upward_trend_threshold, dip_threshold, profit_threshold, stop_loss_threshold, last_operation_price, current_price, is_next_operation_buy):
    upward_trend_threshold = strToFloat(upward_trend_threshold)
    dip_threshold = strToFloat(dip_threshold)
    profit_threshold = strToFloat(profit_threshold)
    stop_loss_threshold = strToFloat(stop_loss_threshold)
    last_operation_price = strToFloat(last_operation_price)
    current_price = strToFloat(current_price)

    percentage_diff = (
        current_price - last_operation_price)/last_operation_price*100
    if is_next_operation_buy:
        last_operation_price, is_next_operation_buy = tryToBuy(
            percentage_diff, upward_trend_threshold, dip_threshold)
    else:
        last_operation_price, is_next_operation_buy = tryToSell(
            percentage_diff, profit_threshold, stop_loss_threshold)

    last_operation_price = floatToStr(last_operation_price)
    is_next_operation_buy = floatToStr(last_operation_price)
    return last_operation_price, is_next_operation_buy


def trackBotInvest():
    # get total invested and what not to move
    my_invest = 300
    currency = 'MXN'
    currency_invested_to = ''
    crypto_amount = ''

    pass
