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


# def tryToBuy(percentage_diff, upward_trend_threshold, dip_threshold):
#     message = ['Percentage difference:', percentage_diff, '%']
#     log_message('INFO', message)
#     if percentage_diff >= upward_trend_threshold or percentage_diff <= dip_threshold:
#         log_message('INFO', 'BUYING')
#         # last_operation_price = api.placeBuyOrder()
#         if last_operation_price['success']:
#             data = utils.historyData(
#                 'BUY', last_operation_price, last_operation_price, percentage_diff)
#         is_next_operation_buy = False
#     return last_operation_price, is_next_operation_buy

def tryToBuy(percentage_diff, upward_trend_threshold, dip_threshold):
    message = ['Percentage difference:', percentage_diff, '%']
    log_message('INFO', message)
    buy = False
    if percentage_diff >= upward_trend_threshold or percentage_diff <= dip_threshold:
        log_message('INFO', 'BUY')
        buy = True
    return True


# def tryToSell(percentage_diff, profit_threshold, stop_loss_threshold):
#     message = ['Percentage difference:', percentage_diff]
#     log_message('INFO', message)
#     if percentage_diff >= profit_threshold or percentage_diff <= stop_loss_threshold:
#         log_message('INFO', 'SELLING')
#         last_operation_price = api.placeSellOrder()
#         is_next_operation_buy = True
#     return last_operation_price, is_next_operation_buy

def tryToSell(percentage_diff, profit_threshold, stop_loss_threshold):
    message = ['Percentage difference:', percentage_diff]
    log_message('INFO', message)
    sell = False
    if percentage_diff >= profit_threshold or percentage_diff <= stop_loss_threshold:
        log_message('INFO', 'SELL')
        sell = True
    return sell


def attemptToMakeTrade(bid_price, ask_price, upward_trend_threshold, dip_threshold, profit_threshold, stop_loss_threshold, last_operation_price, is_next_operation_buy):
    upward_trend_threshold = utils.strToFloat(upward_trend_threshold)
    dip_threshold = utils.strToFloat(dip_threshold)
    profit_threshold = utils.strToFloat(profit_threshold)
    stop_loss_threshold = utils.strToFloat(stop_loss_threshold)
    last_operation_price = utils.strToFloat(last_operation_price)
    bid_price = utils.strToFloat(bid_price)
    ask_price = utils.strToFloat(ask_price)

    acction = False
    if is_next_operation_buy:
        log_message('INFO', 'Next operation is: BUY')
        price_diff = bid_price - last_operation_price
        percentage_diff = price_diff / last_operation_price * 100
        # last_operation_price, is_next_operation_buy = tryToBuy(
        #     percentage_diff, upward_trend_threshold, dip_threshold)
        action = tryToBuy(
            percentage_diff, upward_trend_threshold, dip_threshold)
    else:
        log_message('INFO', 'Next operation is: SELL')
        price_diff = ask_price - last_operation_price
        percentage_diff = price_diff / last_operation_price*100
        # last_operation_price, is_next_operation_buy = tryToSell(
        #     percentage_diff, profit_threshold, stop_loss_threshold)
        action = tryToSell(
            percentage_diff, upward_trend_threshold, dip_threshold)

    # last_operation_price = utils.floatToStr(last_operation_price)
    # is_next_operation_buy = utils.floatToStr(last_operation_price)
    # return last_operation_price, is_next_operation_buy
    return action


def trackBotInvest():
    # get total invested and what not to move
    my_invest = 300
    currency = 'MXN'
    currency_invested_to = ''
    crypto_amount = ''

    pass
