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
        btc_fee = bot.getTakerPercentageFee('btc_mxn')

        # trying to buy
        if is_next_operation_buy:
            btc_bids = bot.getBids('btc_mxn')
            bid_current_price = btc_bids[0]['price']
            btc_mxn = trade.mayorMinorConversion(balance, btc_bids)
            total_btc = trade.tradeWithFee(btc_mxn, btc_fee)

            percentage_diff = trade.percentageDifference(
                bid_current_price, last_operation_price)
            action = trade.tryToBuy(
                percentage_diff, upward_trend_threshold, dip_threshold)
            # buy
            if action:
                message = ['Bot tip: BUY']
                log_message('INFO', message)
                # response = bot.buyMarket('btc_mxn', minor='100.00')
                response = {'success': True}  # supposition
                log_message('INFO', response)
                # if success change is_next operation
                if response['success']:
                    message = ['Bought Currency: BTC']
                    log_message('INFO', message)
                    is_next_operation_buy = False
                    data = utils.historyData('BUY', 'btc_mxn', '100.00', bid_current_price,
                                             total_btc, percentage_diff)
                    utils.cvsFileAppend(data)

                else:
                    message = ['Could NOT BUY currency: BTC']
                    log_message('ERROR', message)

            else:
                message = ['Bot tip: STAY']
                log_message('INFO', message)

        # sell
        else:
            btc_asks = bot.getAsks('btc_mxn')
            ask_current_price = btc_asks[0]['price']

            percentaje_diff = trade.percentageDifference(
                ask_current_price, last_operation_price)
            action = trade.tryToSell(
                percentage_diff, profit_threshold, stop_loss_threshold)
            # sell
            # response = bot.sellMarket('btc_mxn', mayor='')
            # if success change is_next operation
            if response['success']:
                message = ['Sold Currency: BTC']
                log_message('INFO', message)
                is_next_operation_buy = True
            else:
                message = ['Could NOT SELL currency: BTC']
                log_message('ERROR', message)

        utils.sleep(1)


def main():

    is_next_operation_buy = True

    last_operation_price = 100.00

    startBot()


if __name__ == '__main__':
    main()
