from logs import Log
import api
import utils


log = Log()


def tradeWithFee(amount, fee):
    # gives the amount that will be given including the taker or maker fee
    amount = utils.strToFloat(amount)
    fee = utils.strToFloat(fee)

    total = amount - amount * (fee / 100)

    total = utils.floatToStr(total)
    message = ['Trade with fee will give:', total]
    log.message('INFO', message)
    return total


def conversion(buy: bool, amount, books: list):
    amount = utils.strToFloat(amount)
    total = 0
    needed = None
    for book in books:
        price = utils.strToFloat(book['price'])
        if buy:
            total += amount / price
            if not needed:
                needed = total
            if utils.strToFloat(book['amount']) < needed:
                needed -= utils.strToFloat(book['amount'])
            else:
                break
        else:
            total += amount * price
            if not needed:
                needed = amount
            if utils.strToFloat(book['amount']) < needed:
                needed -= utils.strToFloat(book['amount'])
            else:
                break
            break

    total = utils.floatToStr(total)
    message = ['Trade will give:', total]
    log.message('INFO', message)
    return total


def tryToBuy(percentage_diff, upward_trend_threshold, dip_threshold):
    percentage_diff = utils.strToFloat(percentage_diff)
    buy = False
    message = ['Bot tip: STAY']
    if percentage_diff >= upward_trend_threshold or percentage_diff <= dip_threshold:
        message = ['Bot tip: BUY']
        buy = True
    log.message('INFO', message)
    return buy


def tryToSell(percentage_diff, profit_threshold, stop_loss_threshold):
    percentage_diff = utils.strToFloat(percentage_diff)
    sell = False
    message = ['Bot tip: STAY']
    if percentage_diff >= profit_threshold or percentage_diff <= stop_loss_threshold:
        message = ['Bot tip: SELL']
        sell = True
    log.message('INFO', message)
    return sell


def percentageDifference(prior_total, current_total):
    # make sure to compare crypto with crypto and currency with currency
    current_total = utils.strToFloat(current_total)
    prior_total = utils.strToFloat(prior_total)
    difference = current_total - prior_total
    percentage_diff = difference * (prior_total / current_total)
    percentage_diff = utils.floatToStr(percentage_diff)
    message = ['Percentage difference:', percentage_diff, '%']
    log.message('INFO', message)
    return percentage_diff


def attemptToMakeTrade(is_next_operation_buy, percentage_diff, limit_threshold, trend):
    if is_next_operation_buy:
        action = tryToBuy(percentage_diff, limit_threshold, trend)
    else:
        action = tryToSell(percentage_diff, limit_threshold, trend)

    return action


def tradeMessage(is_next_operation_buy, mayor_minor, prev_amount, amount, percentage_diff, total):
    message = ['Operation succesfull']
    log.message('INFO', message)
    if is_next_operation_buy:
        new_currency = 'BTC'
        prev_currency = 'MXN'
        message = ['[BOUGHT] -', mayor_minor.split('_')[0]]
    else:
        new_currency = 'MXN'
        prev_currency = 'BTC'
        message = ['[SOLD] -', mayor_minor.split('_')[1]]
    log.message('INFO', message)
    message = ['[PREV AMOUNT] -', prev_amount, prev_currency]
    log.message('INFO', message)
    message = ['[AMOUNT] -', amount, prev_currency]
    log.message('INFO', message)
    message = ['[% DIFF] -', percentage_diff, '%']
    log.message('INFO', message)
    message = ['[NEW BALANCE] -', total, new_currency]
    log.message('INFO', message)
