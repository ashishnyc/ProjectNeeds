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
        query = """SELECT TABLE_NAME,COLUMN_NAME,DATA_TYPE 
                   FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='{schema}'""".\
            format(schema=self.__database)
        try:
            self.__open()
            self.__db_structure = pd.read_sql(query, con=self.__dbconn)
            self.__close()
        except mdb.Error, e:
            raise e

    def __open(self):
        self.__dbconn = mdb.Connection(self.__host, self.__username, self.__password, self.__database)
        self.__cursor = self.__dbconn.cursor()

    def __close(self):
        self.__cursor.close()
        self.__dbconn.close()

    def __get_column_datatype(self, table_name, column_name):
        return (self.__db_structure[(self.__db_structure['TABLE_NAME'] == table_name)
                                   & (self.__db_structure['COLUMN_NAME'] == column_name)]["DATA_TYPE"].values[0])

    def __create_select_query(self, table_name, column_names, value_filters=None, like_filters=None):
        query = "SELECT "
        query += ','.join(column_names)
        query += " FROM "
        query += table_name
        if value_filters is not None:
            query += " WHERE "
            query += ' AND '.join(["{col}{operator}{value}".
                                  format(col=k
                                         , operator=v[0]
                                         , value="'{0}'".format(v[1]) if self.__get_column_datatype(table_name=table_name
                                                                                                    , column_name=k) == 'varchar' else v[1])
                                   for k, v in value_filters.iteritems()]
                                  )

        if like_filters is not None:
            if value_filters is not None:
                query += " AND "
            else:
                query += " WHERE "
            query += ' AND '.join(["{col} LIKE '{value}'".format(col=k, value=v) for k, v in like_filters.iteritems()])
        return query

    def get_results(self, query):
        try:
            self.__open()
            df = pd.read_sql(query, con=self.__dbconn)
            self.__close()
        except mdb.Error, e:
            raise e
        return df

    def get_values(self, table_name, column_names, value_filters=None, like_filters=None):
        try:
            self.__open()
            df = pd.read_sql(self.__create_select_query(table_name=table_name
                                                        , column_names=column_names
                                                        , value_filters=value_filters
                                                        , like_filters=like_filters), con=self.__dbconn)
            self.__close()
        except mdb.Error, e:
            raise e
        return df

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

