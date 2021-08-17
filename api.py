import config
from iexfinance.stocks import Stock
from iexfinance.refdata import get_symbols
import time
import hmac
import hashlib
import requests
import json
from logs import log
import os
import sys
import itertools


class Bitso:
    def __init__(self, file_path):
        if os.path.isfile(file_path):
            file = open(file_path)
            config = json.load(file)
            file.close()
        else:
            message = ' '.join(['No such file:', file_path])
            sys.exit(message)

        self.__key = config['bitso']['key']
        self.__secret = config['bitso']['secret']
        self.__currency = config['bitso']['currency']
        self.__crypto = config['bitso']['crypto']
        self.__mayor_minor = config['bitso']['mayor_minor']

    @property
    def currency(self):
        return self.__currency

    @property
    def crypto(self):
        return self.__crypto

    @property
    def assets(self):
        assets = self.__currency
        for crypto in self.__crypto:
            assets.append(crypto)
        return assets

    def createSignature(self, http_method, request_path):
        nonce = str(int(round(time.time() * 1000)))
        message = nonce+http_method+request_path
        if (http_method == "POST"):
            message += json.dumps(self.parameters)
        signature = hmac.new(self.__secret.encode('utf-8'),
                             message.encode('utf-8'),
                             hashlib.sha256).hexdigest()

        # Build the auth header
        auth_header = 'Bitso %s:%s:%s' % (self.__key, nonce, signature)

        # Send request
        if (http_method == "GET"):
            response = requests.get(
                "https://api.bitso.com" + request_path, headers={"Authorization": auth_header})
        elif (http_method == "POST"):
            response = requests.post("https://api.bitso.com" + request_path,
                                     json=self.parameters, headers={"Authorization": auth_header})

        return json.loads(response.content.decode('utf8'))

    def getFees(self, currency_fee=[]):
        http_method = 'GET'
        request_path = '/v3/fees/'
        response = self.createSignature(http_method, request_path)
        data = dict()
        if response['success']:
            all_data = dict()
            for balance in response["payload"]["fees"]:
                if balance['book'] in self.__mayor_minor:
                    all_data[balance['book']] = balance
            if currency_fee:
                for c in currency_fee:
                    if c in all_data:
                        data[c] = all_data[c]
                        data[c]['success'] = True
                    else:
                        data[c] = self.emptyBalance(c)
                        message = ' '.join(
                            ['Currency', c, 'not available.'])
                        log('ERROR', message)
            else:
                data = all_data
        return data

    def getBalance(self, currency=[]):
        http_method = 'GET'
        request_path = '/v3/balance/'
        response = self.createSignature(http_method, request_path)

        data = dict()
        if response['success']:
            data['success'] = True
            all_data = dict()
            all_data['success'] = True
            for balance in response["payload"]["balances"]:
                all_data[balance['currency']] = balance
            if currency:
                for c in currency:
                    if c in all_data:
                        data[c] = all_data[c]
                        data[c]['success'] = True
                    else:
                        data[c] = self.emptyBalance(c)
                        message = ' '.join(
                            ['Currency', c, 'not available.'])
                        log('ERROR', message)
            else:
                data = all_data
        else:
            data['success'] = False
            message = 'Unable to connect'
            log('ERROR', message)

        return data

    def emptyBalance(self, currency):
        data = {'currency': currency, 'success': False}
        return data


def getBalances():
    pass


def getMarketPrice():

    get_symbols(output_format='pandas', token=config.TOKEN)
    tsla = Stock('AAPL', token=config.TOKEN)
    # print(tsla.get_quote())
    print(tsla.get_price())


def placeSellOrder():
    pass


def placeBuyOrder():
    pass


def getOperationDetail():
    pass
