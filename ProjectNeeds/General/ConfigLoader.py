#!/usr/bin/python
import ConfigParser
import os
import sys


class ConfigLoader:
    def __init__(self, config_file):
        self.__config = ConfigParser.RawConfigParser()
        if not os.path.isfile(config_file):
            print('config file[{file}] does not exist. Exiting.'.format(file=config_file))
            sys.exit(0)
        self.__config.read(config_file)

    def get(self, section, option):
        return self.__config.get(section=section, option=option)