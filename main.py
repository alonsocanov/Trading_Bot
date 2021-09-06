from logs import Log
import utils
import api
import trade
from trade_history import TradeHistory
from price_history import PriceHistory


def startBot():
    log = Log()
    log.message('INFO', 'Started bot')
    # Bitso information
    bot = api.Bitso('config/credentials.json')
    # trade configuration
    trade_config = utils.readJson('config/trade.json')
    # trade history
    trade_hist = TradeHistory()
    # price histori for further analysis
    price_hist = PriceHistory()

    upward_trend_threshold = trade_config['UPWARD_TREND_THRESHOLD']
    dip_threshold = trade_config['DIP_THRESHOLD']
    profit_threshold = trade_config['PROFIT_THRESHOLD']
    stop_loss_threshold = trade_config['STOP_LOSS_THRESHOLD']

    mayor_minor = 'btc_mxn'

    my_assets = bot.assets
    # get las trade data
    data = trade_hist.getData()
    # if there is not any prior information force to buy crypto
    if not data:
        amount = bot.getBalance('mxn')
        is_next_operation_buy = True
        # in order to determine it shoul actiually buy, 5 day prior analisis must be done
    # if there is prior information set variables
    else:
        amount = data['amount']
        success = data['success']
        is_next_operation_buy = data['transaction']

        is_next_operation_buy = utils.nextOperation(
            success, is_next_operation_buy)

    for idx in range(1):
        # get bid and ask prices for history storage and to determine action
        bid_prices = bot.getBids(mayor_minor)
        ask_prices = bot.getAsks(mayor_minor)
        # buy data
        if is_next_operation_buy:
            # taker fee
            fee = bot.getTakerPercentageFee(mayor_minor)
            # list of current bids
            current_prices = bid_prices
            # current bid
            current_price = bid_prices[0]['price']
            #
            limit_threshold = upward_trend_threshold
            #
            trend = dip_threshold

        # sell data
        else:
            # maker fee
            fee = bot.getMakerPercentageFee(mayor_minor)
            # list of current asks
            current_prices = ask_prices
            # current ask
            current_price = ask_prices[0]['price']
            #
            limit_threshold = profit_threshold
            #
            trend = stop_loss_threshold

        # total amount that would be received if trade is done
        total = trade.conversion(is_next_operation_buy, amount, current_prices)
        total = trade.tradeWithFee(total, fee)

        # sure to compare crypto with crypto and currency with currency
        percentage_diff = trade.percentageDifference(
            data['obtained'], total)

        action = trade.attemptToMakeTrade(
            is_next_operation_buy, percentage_diff, limit_threshold, trend)
        # buy or sell action
        if action:
            # buy
            if is_next_operation_buy:
                # response = bot.buyMarket('btc_mxn', minor='100.00')
                response = {'success': False}  # supposition
            # sell
            else:
                # response = bot.sellMarket('btc_mxn', minor='100.00')
                response = {'success': False}  # supposition

            success = response['success']
            if success:
                trade_hist.setData(success, is_next_operation_buy, mayor_minor,
                                   amount, current_price, total, percentage_diff)
                trade_hist.appendData()

                amount = total
            else:
                message = ['Unable to make trade']
                log.message('ERROR', message)

            is_next_operation_buy = utils.nextOperation(
                success, is_next_operation_buy)

        ask = ask_prices[0]['price']
        bid = bid_prices[0]['price']
        price_hist.setData(bid, ask)
        price_hist.appendData()

        price_hist.plot(3)

        utils.sleep(1)


def main():

    startBot()


if __name__ == '__main__':
    main()
