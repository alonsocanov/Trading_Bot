from logs import log_message
import utils
import api
import trade


def startBot():
    log_message('INFO', 'Started bot')
    bot = api.Bitso('config.json')
    my_assets = bot.assets
    if 'mxn' in my_assets:
        asset = 'mxn'
    balance = bot.getAvailableBalance(asset)
    log_message('INFO', balance)

    for idx in range(5):
        btc_fee = bot.getTakerPercentageFee('btc_mxn')
        btc_bid = bot.getBids('btc_mxn')[0]

        btc_mxn = trade.conversion(balance, btc_bid['price'])
        total_btc = trade.tradeWithFee(btc_mxn, btc_fee)

        utils.sleep(2)


def main():

    is_next_operation_buy = True

    last_operation_price = 100.00

    startBot()


if __name__ == '__main__':
    main()
