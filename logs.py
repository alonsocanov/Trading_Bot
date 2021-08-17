import logging


# log configuration
level = logging.INFO
log_path = ''
logging.basicConfig(filename=log_path, format='%(levelname)s - %(asctime)s - %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S', level=level)


def log(message_type, message):
    message_type = message_type.upper()
    if message_type == 'INFO':
        logging.info(message)
    elif message_type == 'WARNING':
        logging.warning(message)
    elif message_type == 'ERROR':
        logging.error(message)
    elif message_type == 'DEBUG':
        logging.debug(message)

# A good log example
# [BALANCE] USD Balance = 22.15$
# [BUY] Bought 0.002 BTC for 22.15 USD
# [PRICE] Last Operation Price updated to 11,171.40 (BTC/USD)
# [ERROR] Could not perform SELL operation - Insufficient balance
