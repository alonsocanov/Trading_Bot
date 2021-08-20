from logs import log_message
import utils
import api


def startBot():
    log_message('INFO', 'Started bot')
    bot = api.Bitso('config.json')
    my_assets = bot.assets
    if 'mxn' in my_assets:
        asset = 'mxn'
    balance = bot.getBalance(asset)
    log_message('INFO', balance)

    # fees = bot.getFees()
    # trades = bot.getTrades()
    # orders = bot.getOrder()
    # available_books = bot.getAvailableBooks(['btc_mxn'])
    # ticker = bot.getTicker()
    # order_book = bot.getOrederBook('btc_mxn')
    # print(balance)
    # print('\n')
    # print(available_books)
    # print('\n')
    # print(ticker)
    # print('\n')
    # print(order_book)


def main():

    is_next_operation_buy = True

    last_operation_price = 100.00

    startBot()


if __name__ == '__main__':
    main()
