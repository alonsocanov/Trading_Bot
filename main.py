from logs import log_message
import utils
import api
import trade


def startBot():
    log_message('INFO', 'Started bot')
    bot = api.Bitso('config/credentials.json')
    trade_config = utils.readJson('config/trade.json')

    upward_trend_threshold = trade_config['UPWARD_TREND_THRESHOLD']
    dip_threshold = trade_config['DIP_THRESHOLD']
    profit_threshold = trade_config['PROFIT_THRESHOLD']
    stop_loss_threshold = trade_config['STOP_LOSS_THRESHOLD']

    mayor_minor = 'btc_mxn'

    my_assets = bot.assets
    if 'mxn' in my_assets:
        asset = 'mxn'
    balance = bot.getAvailableBalance(asset)
    btc_bids = bot.getBids('btc_mxn')
    last_operation_price = btc_bids[0]['price']

    is_next_operation_buy = True

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

        btc_mxn = trade.mayorMinorConversion(balance, current_prices)

        total_btc = trade.tradeWithFee(btc_mxn, fee)
        # this percentage difference is incorrect mus compare
        percentage_diff = trade.percentageDifference(
            current_price, last_operation_price)

        action = trade.attemptToMakeTrade(
            is_next_operation_buy, percentage_diff, limit_threshold, trend)
        # buy or sell action
        if action:
            if is_next_operation_buy:
                message = ['Bot tip: BUY']
                log_message('INFO', message)
                # response = bot.buyMarket('btc_mxn', minor='100.00')
                response = {'success': True}  # supposition
            else:
                message = ['Bot tip: SELL']
                log_message('INFO', message)
                # response = bot.sellMarket('btc_mxn', minor='100.00')
                response = {'success': True}  # supposition
                log_message('INFO', response)
            is_next_operation_buy = utils.saveHistory(response['success'], 'BUY', 'btc_mxn',
                                                      '100.00', current_price, total_btc, percentage_diff)
        else:
            message = ['Bot tip: STAY']
            log_message('INFO', message)

        utils.sleep(1)


def main():

    is_next_operation_buy = True

    last_operation_price = 100.00

    startBot()


if __name__ == '__main__':
    main()
