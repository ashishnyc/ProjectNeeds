#!/usr/bin/python
import MySQLdb as mdb
import ConfigParser, os, sys
'''
    Database connection class
'''
dbConn=None

class MySqlConnection:
    def __init__(self, ConfigFile):
        self.__config = ConfigParser.RawConfigParser()
        self.__ConfigFile = ConfigFile
        if not os.path.isfile(self.__ConfigFile):
            print('ConfigFile[{0}] does not exist. Exiting.'.format(self.__ConfigFile))
            sys.exit(0)
        self.__config.read(self.__ConfigFile)
        self.__host = self.__config.get('DATABASE', 'HOST')
        self.__port = self.__config.get('DATABASE', 'PORT')
        self.__username = self.__config.get('DATABASE', 'USERNAME')
        self.__password = self.__config.get('DATABASE', 'PASSWORD')
        self.__database = self.__config.get('DATABASE', 'DATABASE')

    def __open(self):
        try:
            self.__dbconn = mdb.Connection(self.__host, self.__username, self.__password, self.__database)
            self.__cursor = self.__dbconn.cursor()
        except mdb.Error as e:
            print(str(e))

    def __close(self):
        self.__cursor.close()
        self.__dbconn.close()

    def getoneresult(self, query):
        try:
            self.__open()
            self.__cursor.execute(query)
            result = self.__cursor.fetchone()
            self.__close()
        except Exception as e:
            print(str(e))
        return result

    def getmultipleresults(self, query):
        try:
            self.__open()
            self.__cursor.execute(query)
            result = self.__cursor.fetchall()
            self.__close()
        except Exception as e:
            print(str(e))
        return result

    def insertrecord(self, query):
        try:
            self.__open()
            ret_value = self.__cursor.execute(query)
            self.__dbconn.commit()
            self.__close()
            return ret_value
        except Exception as e:
            print(str(e))

    def insertmultipleresults(self, query, data):
        try:
            self.__open()
            self.__cursor.executemany(query, data)
            self.__dbconn.commit()
            self.__close()
        except Exception as e:
            print(str(e))

    def get_conn(self):
        return mdb.Connection(self.__host, self.__username, self.__password, self.__database)