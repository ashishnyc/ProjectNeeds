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
        self.__configfile = ConfigFile
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
            self.__Logger.error("Error occurred while opening sql connection")

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
            self.__Logger("Error occurred while running query[{0}], {1}".format(query, str(e)))
        return result

    def getmultipleresults(self, query):
        try:
            self.__open()
            self.__cursor.execute(query)
            result = self.__cursor.fetchall()
            self.__close()
        except Exception as e:
            self.__Logger("Error occurred while running query[{0}], {1}".format(query, str(e)))
        return result

    def insertrecord(self, query):
        try:
            self.__open()
            self.__cursor.execute(query)
            self.__dbconn.commit()
            self.__close()
        except Exception as e:
            self.__Logger("Error occurred while running query[{0}], {1}".format(query, str(e)))

    def insertmultipleresults(self, query, data):
        try:
            self.__open()
            self.__cursor.executemany(query, data)
            self.__dbconn.commit()
            self.__close()
        except Exception as e:
            self.__Logger("Error occurred while running query[{0}], {1}".format(query, str(e)))
