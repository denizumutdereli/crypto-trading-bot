import os
import sys
import datetime
from modules import Settings as settings
from rich import print
from rich.pretty import pprint
from rich.progress import track
import codecs
import json
from datetime import datetime
from pathlib import Path
import logging as log

class Config():
    constants = {
    "max_open_trades" : 1,
    "stake_currency" : "USDT",
    "stake_amount": 0,
    "tradable_balance_ratio" : 0.99,
    "last_stake_amount_min_ratio" : 0.1,
    "fiat_display_currency" : "USD",
    "timeframe": "5m",
    "cancel_open_orders_on_exit" : "false",
    "exchange" : {},
    "bot_name" : "abot",
    "pairlists" : [],
    }
    Validation  = True
    logger = log.getLogger("Config")
    setting = {}

    def __init__(self, file, settings):
        self.time_offset = 0
        self.loadConfigFile(file,settings)
        
       
    def loadConfigFile(self,file, settings):
        # config versions
        # now = datetime.now()
        # datetimeFormat = '%Y/%m/%d %H:%M:%S.%f'
        # dt_string = now.strftime(datetimeFormat)
        configFile = Path(settings.root + "config/"+file+'.json')
        if configFile.is_file():
            with codecs.open(configFile, mode='r',encoding='utf-8') as cache:
                configCache = json.load(cache)
                if self.validateRules(configCache) != False:
                    self.__dict__ = configCache
                    self.settings = settings
                else:
                    exit()
        else:
            self.logger.critical('Could not find the "'+str(file)+'" config file.')
            exit()
    
    def validateRules(self, config):
        #constants
        for i in self.constants:
            if i not in config:
                self.logger.warning('Could not find "' + i + '" parameter in config file.')
                self.Validation = False
        #valuescheck
        if config['max_open_trades'] == 0:
            self.logger.info('Setting up max_open_trades to 0 will not effect. Your value is ' + str(config['max_open_trades']))
            self.Validation = False
        elif config['max_open_trades'] < 1:
            self.logger.warning('Setting up max_open_trades negative number will not effect. Your value is ' + str(config['max_open_trades']))
            self.Validation = False
        elif config['stake_currency'] == "":
            self.logger.warning('Setting "stake_currency" is mandatory. You are recommended to use "'+self.constants['stake_currency']+'"')
            self.Validation = False
        #...
        # other validation rules will be added
       
        return self.Validation