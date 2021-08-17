import logs
import utils
import api


def startBot():
    bot = api.Bitso('config.json')
    balance = bot.getBalance(bot.assets)
    fees = bot.getFees(['btc_mxn'])
    print(fees)


def main():

    is_next_operation_buy = True

    last_operation_price = 100.00

    startBot()


if __name__ == '__main__':
    main()
