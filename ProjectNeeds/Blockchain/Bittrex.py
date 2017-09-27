#!/usr/bin/python
import sys, os, ConfigParser


class Bittrex:

    def __init__(self, ConfigFile):
        self.__config = ConfigParser.RawConfigParser()
        if not os.path.isfile(ConfigFile):
            print('ConfigFile[{0}] does not exist. Exiting.'.format(ConfigFile))
            sys.exit(0)
        self.__config.read(ConfigFile)
        self.__uri = "https://bittrex.com/api/"
        self.__apikey = self.__config.get('BITTREX', 'API_KEY')
        self.__version = self.__config.get('BITTREX', 'VERSION')
        self.__apisecret = self.__config.get('BITTREX', 'API_SECRET')

    def __createurl(self, method, options = None):
        print(method)

    def get
