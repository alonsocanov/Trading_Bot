from logs import log_message
import utils
import api
import trade


def startBot():
    log_message('INFO', 'Started bot')
    bot = api.Bitso('config/credentials.json')
    trade_config = utils.readJson('config/trade.json')

    history_file = utils.createFile('data', 'json')

    upward_trend_threshold = trade_config['UPWARD_TREND_THRESHOLD']
    dip_threshold = trade_config['DIP_THRESHOLD']
    profit_threshold = trade_config['PROFIT_THRESHOLD']
    stop_loss_threshold = trade_config['STOP_LOSS_THRESHOLD']

    my_assets = bot.assets
    if 'mxn' in my_assets:
        asset = 'mxn'
    balance = bot.getAvailableBalance(asset)
    btc_bids = bot.getBids('btc_mxn')
    last_operation_price = btc_bids[0]['price']

    is_next_operation_buy = True

    for idx in range(1):
        btc_fee = bot.getTakerPercentageFee('btc_mxn')
        btc_bids = bot.getBids('btc_mxn')
        btc_asks = bot.getAsks('btc_mxn')
        bid_current_price = btc_bids[0]['price']
        ask_current_price = btc_asks[0]['price']
        btc_mxn = trade.mayorMinorConversion(balance, btc_bids)
        total_btc = trade.tradeWithFee(btc_mxn, btc_fee)
        # last_operation_price, is_next_operation_buy = trade.attemptToMakeTrade(bid_current_price, ask_current_price,
        #                                                                        upward_trend_threshold, dip_threshold, profit_threshold, stop_loss_threshold,
        #                                                                        last_operation_price, is_next_operation_buy)
        action = trade.attemptToMakeTrade(bid_current_price, ask_current_price,
                                          upward_trend_threshold, dip_threshold, profit_threshold, stop_loss_threshold,
                                          last_operation_price, is_next_operation_buy)

        if action and is_next_operation_buy:
            # buy
            response = bot.buyMarket('btc_mxn')
            log_message('INFO', response)
            # if success change is_next operation
            if response['success']:
                message = ['Bought Currency: BTC']
                log_message('INFO', message)
                is_next_operation_buy = False
            else:
                message = ['Could NOT BUY currency: BTC']
                log_message('ERROR', message)

        elif action and not is_next_operation_buy:
            response = bot.sellMarket('btc_mxn')
            # if success change is_next operation
            if response['success']:
                message = ['Sold Currency: BTC']
                log_message('INFO', message)
                is_next_operation_buy = True
            else:
                message = ['Could NOT SELL currency: BTC']
                log_message('ERROR', message)

        utils.sleep(2)


def main():

    is_next_operation_buy = True

    last_operation_price = 100.00

    startBot()


if __name__ == '__main__':
    main()
