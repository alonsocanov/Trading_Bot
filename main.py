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
    grad = None
    prev_amount = None
    # if there is not any prior information force to buy crypto
    if not data:
        amount = bot.getBalance('mxn')
        is_next_operation_buy = True
        # in order to determine it should actiually buy when no data is available
        grad = price_hist.gradient(5)
    # if there is prior information set variables
    else:
        success = data['success']
        is_next_operation_buy = data['transaction']
        amount = data['obtained']
        prev_amount = data['amount']

        is_next_operation_buy = utils.nextOperation(
            success, is_next_operation_buy)

    message = ['Available amount to trade:', amount]
    log.message('INFO', message)

    while True:
        try:
            # get bid and ask prices for history storage and to determine action
            bid_prices = bot.getBids(mayor_minor)
            ask_prices = bot.getAsks(mayor_minor)
            # buy data
            if is_next_operation_buy:
                message = ['Trying to Buy']
                log.message('INFO', message)
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
                message = ['Trying to Sell']
                log.message('INFO', message)
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
            total = trade.conversion(
                is_next_operation_buy, amount, current_prices)
            total = trade.tradeWithFee(total, fee)

            if not prev_amount:
                grad = price_hist.gradient(num_days=3)
                if grad > 0 and is_next_operation_buy:
                    action = True
                elif grad < 0 and not is_next_operation_buy:
                    action = True
                else:
                    action = False
            else:
                percentage_diff = trade.percentageDifference(
                    prev_amount, total)
                # get sell or buy action
                action = trade.attemptToMakeTrade(
                    is_next_operation_buy, percentage_diff, limit_threshold, trend)
            # buy or sell action
            if action:
                # buy
                if is_next_operation_buy:
                    # response = bot.buyMarket('btc_mxn', minor='100.00')
                    response = {'success': True}  # supposition
                # sell
                else:
                    # response = bot.sellMarket('btc_mxn', minor='100.00')
                    response = {'success': True}  # supposition

                success = response['success']
                if success:
                    trade_hist.setData(success, is_next_operation_buy, mayor_minor,
                                       amount, current_price, total, percentage_diff)
                    trade_hist.appendData()

                    trade.tradeMessage(
                        is_next_operation_buy, mayor_minor, prev_amount, amount, percentage_diff, total)

                    prev_amount = amount
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

            utils.sleep(3600)
        except KeyboardInterrupt:
            message = ['Keyborad interrupt']
            log.message('WARNING', message)
            break


def main():

    startBot()


if __name__ == '__main__':
    main()
