import config
import api


def tryToBuy(percentage_diff):
    if percentage_diff >= config.UPWARD_TREND_THRESHOLD or percentage_diff <= config.DIP_THRESHOLD:
        last_operation_price = api.placeBuyOrder()
        is_next_operation_buy = False
    return last_operation_price, is_next_operation_buy


def tryToSell(percentage_diff):
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
