#!/usr/bin/python
import MySQLdb as mdb
import ConfigParser
import os
import sys
import pandas as pd

'''
    Database connection class
'''
dbConn = None


class MySqlConnection:
    def __init__(self, config_file):
        self.__config = ConfigParser.RawConfigParser()
        if not os.path.isfile(config_file):
            print('config file[{file}] does not exist. Exiting.'.format(file=config_file))
            sys.exit(0)
        self.__config.read(config_file)
        self.__host = self.__config.get('DATABASE', 'HOST')
        self.__port = self.__config.get('DATABASE', 'PORT')
        self.__username = self.__config.get('DATABASE', 'USERNAME')
        self.__password = self.__config.get('DATABASE', 'PASSWORD')
        self.__database = self.__config.get('DATABASE', 'DATABASE')

    def __open(self):
        self.__dbconn = mdb.Connection(self.__host, self.__username, self.__password, self.__database)
        self.__cursor = self.__dbconn.cursor()

    def __close(self):
        self.__cursor.close()
        self.__dbconn.close()

    def get_records(self, query):
        try:
            self.__open()
            df = pd.read_sql(query, con=self.__dbconn)
            self.__close()
        except mdb.Error, e:
            raise e
        return df

    def insert_records(self, query, data=None):
        try:
            self.__open()
            if data is None:
                ret_value = self.__cursor.execute(query)
            else:
                self.__cursor.executemany(query, data)
            self.__dbconn.commit()
            self.__close()
            return ret_value
        except Exception as e:
            print(str(e))

