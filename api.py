import config
# from iexfinance.stocks import Stock
# from iexfinance.refdata import get_symbols
import time
import hmac
import hashlib
import requests
import json
from logs import log_message
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

    def getSignature(self, request_path):
        http_method = 'GET'
        nonce = str(int(round(time.time() * 1000)))
        message = nonce+http_method+request_path
        signature = hmac.new(self.__secret.encode('utf-8'),
                             message.encode('utf-8'),
                             hashlib.sha256).hexdigest()
        # Build the auth header
        auth_header = 'Bitso %s:%s:%s' % (self.__key, nonce, signature)
        response = requests.get(
            "https://api.bitso.com" + request_path, headers={"Authorization": auth_header})
        return json.loads(response.content.decode('utf8'))

    def deleteSignature(self, request_path):
        http_method = 'DELETE'
        nonce = str(int(round(time.time() * 1000)))
        message = nonce+http_method+request_path
        signature = hmac.new(self.__secret.encode('utf-8'),
                             message.encode('utf-8'),
                             hashlib.sha256).hexdigest()
        # Build the auth header
        auth_header = 'Bitso %s:%s:%s' % (self.__key, nonce, signature)
        response = requests.delete(
            "https://api.bitso.com" + request_path, headers={"Authorization": auth_header})
        return json.loads(response.content.decode('utf8'))

    def postSignature(self, request_path, parameters):
        http_method = 'POST'
        nonce = str(int(round(time.time() * 1000)))
        message = nonce+http_method+request_path

        message += json.dumps(parameters)
        signature = hmac.new(self.__secret.encode('utf-8'),
                             message.encode('utf-8'),
                             hashlib.sha256).hexdigest()

        # Build the auth header
        auth_header = 'Bitso %s:%s:%s' % (self.__key, nonce, signature)

        # Send request
        response = requests.post("https://api.bitso.com" + request_path,
                                 json=self.parameters, headers={"Authorization": auth_header})

        return json.loads(response.content.decode('utf8'))

    def getFees(self, currency_fee=[]):
        request_path = '/v3/fees/'
        response = self.getSignature(request_path)
        data = dict()
        if response['success']:
            all_data = dict()
            for balance in response["payload"]["fees"]:
                if balance['book'] in self.__mayor_minor:
                    all_data[balance['book']] = balance
            if currency_fee:
                if isinstance(currency_fee, str):
                    currency_fee = currency_fee.replace(
                        ' ', '').strip(',').split(',')
                for c in currency_fee:
                    if c in all_data:
                        data[c] = all_data[c]
                        data[c]['success'] = True
                    else:
                        data[c] = self.emptyBalance(c)
                        message = ' '.join(
                            ['Currency', c, 'not available.'])
                        log_message('ERROR', message)
            else:
                data = all_data
        return data

    def getBalance(self, currency=[]):
        request_path = '/v3/balance/'
        response = self.getSignature(request_path)

        data = dict()
        if response['success']:
            data['success'] = True
            all_data = dict()
            all_data['success'] = True
            for balance in response["payload"]["balances"]:
                all_data[balance['currency']] = balance
            if currency:
                if isinstance(currency, str):
                    currency = currency.replace(' ', '').strip(',').split(',')
                for c in currency:
                    if c in all_data:
                        data[c] = all_data[c]
                        data[c]['success'] = True
                    else:
                        data[c] = self.emptyBalance(c)
                        message = ' '.join(
                            ['Currency', c, 'not available.'])
                        log_message('ERROR', message)
            else:
                data = all_data
        else:
            data['success'] = False
            message = 'Unable to connect'
            log_message('ERROR', message)

        return data

    def getTrades(self, date=[]):
        request_path = '/v3/user_trades/'
        response = self.getSignature(request_path)
        return response

    def emptyBalance(self, currency):
        data = {'currency': currency, 'success': False}
        return data

    def placeOrder(self, book, side, order_type, price='', mayor='', minor='', time_in_force='', stop=''):
        request_path = '/v3/orders/'
        parameters = dict()
        # book to use (eth_mxn, btc_mxn)
        parameters['book'] = book
        # side of market (buy or sell)
        parameters['side'] = side
        # type of order (limit or market)
        # limit: value reaches a threshold
        # market: current price
        parameters['type'] = order_type
        # the amount of mayor currency
        # the amount of minor currency
        # only amount of minor or mayor can be set
        if mayor and minor:
            message = 'Mayor and minor have values'
            sys.exit(message)
        elif mayor:
            parameters['mayor'] = mayor
        elif minor:
            parameters['minor'] = minor

        # only use price when type is limit
        if order_type == 'limit':
            if isinstance(price, float) and price:
                price = str(price)
            parameters['price'] = price
            # time that the order can be open
            parameters['time_in_force'] = time_in_force
        # only use stop for stop orders
        # determine the price per unit of mayor
        if parameters['mayor'] and stop:
            parameters['stop'] = stop

        response = self.postSignature(self, request_path, parameters)
        return response

    def buyMarket(self, book):
        side = 'buy'
        order_type = 'market'
        response = self.placeOrder(book, side, order_type)
        return response

    def buyLimit(self, book, price, mayor, minor, time_in_force):
        side = 'buy'
        order_type = 'limit'
        response = self.placeOrder(
            book, side, order_type, price, mayor, minor, time_in_force)
        return response

    def getOrder(self, order_id=''):
        request_path = '/v3/orders/'
        ids = Bitso.arrangeRequest(order_id)
        if ids:
            request_path = '/v3/orders/' + ids
        else:
            request_path = '/v3/open_orders/'
        response = self.getSignature(request_path)
        return response

    def cancelOrder(self, order_id):
        ids = Bitso.arrangeRequest(order_id)
        if ',' in ids:
            request_path = '/v3/orders?oids='+ids
        else:
            request_path = '/v3/orders/'+ids
        response = self.deleteSignature(request_path)
        return response

    @staticmethod
    def getPublic(request_path):
        response = requests.get(
            "https://api.bitso.com" + request_path)
        return json.loads(response.content.decode('utf8'))

    @staticmethod
    def arrangeRequest(data):
        arranged_data = ''
        if data:
            if isinstance(data, str):
                # check if thre are multiple (,)
                arranged_data = data.strip(' /,')
            # multiple ids
            elif isinstance(data, list):
                arranged_data = ','.join(data).strip(' ,')
        return arranged_data

    def getAvailableBooks(self, books=''):
        request_path = '/v3/available_books/'
        response = Bitso.getPublic(request_path)
        data = dict()
        if response['success']:
            all_data = dict()
            for balance in response["payload"]:
                if balance['book'] in books:
                    all_data[balance['book']] = balance
            if books:
                if isinstance(books, str):
                    books = books.replace(' ', '').strip(',').split(',')
                for book in books:
                    if book in all_data:
                        data[book] = all_data[book]
                        data[book]['success'] = True
                    else:
                        data[book] = self.emptyBalance(book)
                        message = ' '.join(
                            ['Book', book, 'not available.'])
                        log_message('ERROR', message)
            else:
                data = all_data
        return data

    def getTicker(self, book=''):
        # trading information of a book
        request_path = '/v3/ticker/'
        response = Bitso.getPublic(request_path)

        if response['success']:

            # finish

            pass
        return response

    def getOrederBook(self, book):
        request_path = '/v3/order_book/?book=' + book
        response = Bitso.getPublic(request_path)

        return response


def getBalances():
    pass


def getMarketPrice():
    pass


def getOperationDetail():
    pass
