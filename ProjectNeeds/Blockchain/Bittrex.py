#!/usr/bin/python
import sys, os, ConfigParser
import time, hmac, hashlib, requests

class Bittrex:

    def __init__(self, ConfigFile):
        self.__config = ConfigParser.RawConfigParser()
        if not os.path.isfile(ConfigFile):
            print('ConfigFile[{0}] does not exist. Exiting.'.format(ConfigFile))
            sys.exit(0)
        self.__config.read(ConfigFile)
        self.__uri = "https://bittrex.com/api"
        self.__apikey = self.__config.get('BITTREX', 'API_KEY')
        self.__version = self.__config.get('BITTREX', 'VERSION')
        self.__apisecret = self.__config.get('BITTREX', 'API_SECRET')

    def __getRequestOutput(self, method, options = None):
        optString = ''
        nonce = str(int(time.time() * 1000))
        if options is not None:
            optString='?{0}&apikey={1}&nonce={2}'.format('&'.join(['{0}={1}'.format(i,options[i]) for i in options]),
                                              self.__apikey, nonce)
        url = '{0}/{1}/{2}{3}'.format(self.__uri,self.__version,method,optString)

        sign = hmac.new(self.__apisecret, url, hashlib.sha512).hexdigest()
        req = requests.get(url) if options is None else requests.get(url, headers={'apisign': sign})
        reqJson = req.json()
        if reqJson['success']:
            return reqJson['result']
        return None

    def getMarkets(self):
        return self.__getRequestOutput(method='public/getmarkets')

    def getCurrencies(self):
        return self.__getRequestOutput(method='public/getcurrencies')

    def getTicker(self):
        return self.__getRequestOutput(method='public/getticker')

    def getMarketSummaries(self):
        return self.__getRequestOutput(method='public/getmarketsummaries')

    def getMarketSummary(self, market):
        return  self.__getRequestOutput(method='public/getmarketsummary', options={'market': market})

    def getOrderBook(self, market, side='both'):
        return self.__getRequestOutput(method='public/getorderbook', options={'market':market, 'type':side})

    def getMarketHistory(self, market):
        return self.__getRequestOutput(method='public/getmarkethistory', options={'market':market})

    def buy(self, market, quantity, price):
        return self.__getRequestOutput(method='market/buylimit', options={'market':market,
                                                                          'quantity': quantity, 'rate':price})

    def sell(self, market, quantity, price):
        return self.__getRequestOutput(method='market/selllimit', options={'market':market,
                                                                          'quantity': quantity, 'rate':price})
    def cancel(self, uuid):
        return self.__getRequestOutput(method='market/cancel', options={'uuid':uuid})

    def getMarketOpenOrders(self, market):
        if market is not None:
            return self.__getRequestOutput(method='market/getopenorders', options={'market': market})
        return self.__getRequestOutput(method='market/getopenorders', options={})

    def getBalances(self):
        return self.__getRequestOutput(method='account/getbalances', options={})

    def getBalance(self, market):
        return self.__getRequestOutput(method='account/getbalance', options={'currency': market})

