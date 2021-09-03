from logs import log_message
import utils
import api
import trade
import trade_history


def startBot():
    log_message('INFO', 'Started bot')
    bot = api.Bitso('config/credentials.json')
    trade_config = utils.readJson('config/trade.json')
    history = trade_history.TradeHistory()

    upward_trend_threshold = trade_config['UPWARD_TREND_THRESHOLD']
    dip_threshold = trade_config['DIP_THRESHOLD']
    profit_threshold = trade_config['PROFIT_THRESHOLD']
    stop_loss_threshold = trade_config['STOP_LOSS_THRESHOLD']

    mayor_minor = 'btc_mxn'

    my_assets = bot.assets

    data = history.getData()
    amount = data['amount']
    if not data:
        amount = bot.getBalance('mxn')

    is_next_operation_buy = utils.nextOperation(
        data['success'], data['transaction'])

    for idx in range(1):
        # buy data
        if is_next_operation_buy:
            # taker fee
            fee = bot.getTakerPercentageFee('btc_mxn')
            # list of current bids
            current_prices = bot.getBids('btc_mxn')
            # current bid
            current_price = current_prices[0]['price']
            #
            limit_threshold = upward_trend_threshold
            #
            trend = dip_threshold

        # sell data
        else:
            # maker fee
            fee = bot.getMakerPercentageFee('btc_mxn')
            # list of current asks
            current_prices = bot.getAsks('btc_mxn')
            # current ask
            current_price = current_prices[0]['price']

            limit_threshold = profit_threshold
            trend = stop_loss_threshold

        total = trade.conversion(amount, current_prices)
        total = trade.tradeWithFee(total, fee)
        print(data)

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

            if response['success']:
                history.setData(response['success'], is_next_operation_buy, mayor_minor,
                                amount, current_price, total, percentage_diff)
                history.appendData()
            else:
                message = ['Unable to make trade']
                log_message('ERROR', message)

            is_next_operation_buy = utils.nextOperation(
                response['success'], is_next_operation_buy)

        utils.sleep(1)


def main():

    startBot()


if __name__ == '__main__':
    main()
