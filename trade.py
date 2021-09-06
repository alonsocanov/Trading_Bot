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


def conversion(amount, books: list, buy: bool):
    amount = utils.strToFloat(amount)
    total = 0
    needed = None
    for book in books:
        price = utils.strToFloat(book['price'])
        if buy:
            total += amount / price
        else:
            total += amount * price
        if not needed:
            needed = total
        if utils.strToFloat(book['amount']) < needed:
            needed -= utils.strToFloat(book['amount'])
        else:
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
    current_total = utils.strToFloat(current_total)
    prior_total = utils.strToFloat(prior_total)
    percentage_diff = -1 * (100.0 - (current_total * 100.0 / prior_total))
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
