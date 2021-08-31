from logs import log_message
import api
import utils


def tradeWithFee(amount, fee):
    # gives the amount that will be given including the taker or maker fee
    amount = utils.strToFloat(amount)
    fee = utils.strToFloat(fee)

    total = amount - amount * (fee / 100)

    total = utils.floatToStr(total)
    message = ['Trade with fee will give:', total]
    log_message('INFO', message)
    return total


def mayorMinorConversion(amount, books: list):
    amount = utils.strToFloat(amount)
    total = 0
    needed = None
    for book in books:
        price = utils.strToFloat(book['price'])
        total += amount / price
        if not needed:
            needed = total
        if utils.strToFloat(book['amount']) < needed:
            needed -= utils.strToFloat(book['amount'])
        else:
            break

    total = utils.floatToStr(total)
    message = ['Trade will give:', total]
    log_message('INFO', message)
    return total


def tryToBuy(percentage_diff, upward_trend_threshold, dip_threshold):
    percentage_diff = utils.strToFloat(percentage_diff)
    message = ['Percentage difference:', percentage_diff, '%']
    log_message('INFO', message)
    buy = False
    if percentage_diff >= upward_trend_threshold or percentage_diff <= dip_threshold:
        log_message('INFO', 'BUY')
        buy = True
    return True


def tryToSell(percentage_diff, profit_threshold, stop_loss_threshold):
    percentage_diff = utils.strToFloat(percentage_diff)
    message = ['Percentage difference:', percentage_diff]
    log_message('INFO', message)
    sell = False
    if percentage_diff >= profit_threshold or percentage_diff <= stop_loss_threshold:
        log_message('INFO', 'SELL')
        sell = True
    return sell


def percentageDifference(price, last_operation_price):
    message = ['Current market price:', price]
    log_message('INFO', message)
    message = ['Last operation price:', last_operation_price]
    log_message('INFO', message)
    price = utils.strToFloat(price)
    last_operation_price = utils.strToFloat(last_operation_price)
    price_diff = price - last_operation_price
    percentage_diff = price_diff / last_operation_price * 100
    percentage_diff = utils.floatToStr(percentage_diff)
    message = ['Percentage difference:', price_diff, '%']
    log_message('INFO', message)
    return percentage_diff


def attemptToMakeTrade(is_next_operation_buy, percentage_diff, limit_threshold, trend):
    if is_next_operation_buy:
        action = tryToBuy(percentage_diff, limit_threshold, trend)
    else:
        action = tryToSell(percentage_diff, limit_threshold, trend)
    return action


def trackBotInvest():
    # get total invested and what not to move
    my_invest = 300
    currency = 'MXN'
    currency_invested_to = ''
    crypto_amount = ''

    pass
