#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from configparser import ConfigParser
from Definition import ROOT_CONFIG_INI
from WebSocket import Okcoin

# Singleton implementation to read only once the fees.ini
class APIs:

    # Create inner private class to get the first initialization of the fees object
    class __APIs:
        def __init__(self):
            parser = ConfigParser()
            parser.read(ROOT_CONFIG_INI)


            self.APIsWs = {
                'Okcoin': Okcoin.Okcoin(parser.get('OkcoinWebSocket', 'key'), parser.get('OkcoinWebSocket', 'secret'), parser.get('OkcoinWebSocket', 'url'))
            }
    __instance = None

    def __init__(self):
        # Instance instance object to create the singleton object.
        if not APIs.__instance:
            APIs.__instance = APIs.__APIs()

    def getAPIsWs(self):
        return self.__instance.APIsWs