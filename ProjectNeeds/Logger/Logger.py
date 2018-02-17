#!/usr/bin/python
import os
import sys
from datetime import datetime


class Logger:
    def __init__(self, path, name):
        if not os.path.isdir(path):
            print("Path[{path}] does not seems to exist.".format(path=path))
            sys.exit()

        self.__filename = "{path}/{filename}_{date}.log".format(path=path, filename=name
                                                                , date=datetime.now().strftime("%Y%m%d"))
        self.write_msg(logtype="START", msg="********** starting {filename}**********".format(filename=self.__filename))

    def write_msg(self, logtype="", msg=""):
        f = open(name=self.__filename, mode='a')
        log = "{ts} {logtype:<10} {msg}\n".format(ts=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                                  , logtype=logtype, msg=msg)
        f.writelines(log)
        f.close()

    def error(self, msg):
        self.write_msg(logtype="ERROR", msg=msg)

    def info(self, msg):
        self.write_msg(logtype="INFO", msg=msg)
