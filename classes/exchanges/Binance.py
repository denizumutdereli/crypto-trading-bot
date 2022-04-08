import ccxt
from ccxt import AuthenticationError
import logging as log
import modules.menu as menu
import time
import json
from rich import print
from rich.pretty import pprint
from classes.Log import Log
from classes.State import State

class Binance(State):
   
    def __init__(self, config, sync = False):
        logger = log.getLogger('Exchange -' + config.exchange.name)
        #binance = ccxt.binance({'nonce': ccxt.Exchange.milliseconds}) Sending request more then 1+/sec
        self.time_offset = 0
        self.connect(config)

        if sync:
            self.time_offset = self._get_time_offset()

    #Binance connection
    def connect(self, config):
        self.__dict__ = config.exchange
        self.logger.info('Connecting to ' + self.name)
  
        if config.sandbox == True:
            try:
                self.client = ccxt.binance({'apiKey': self.sandbox_key,'secret': self.sandbox_secret, "API_URL" : self.sandbox_api})
                self.logger.info('Connection successful. Sandbox Api')
            except AuthenticationError as e:
                self.logger.exception(e)
                exit()
        else:
            #play("alert")
            self.logger.warn('Caution, you have selected real trade api option.')
            if config.settings.accept == 0:
                answer = menu.yes_or_no("Please confirm the real trade api option:")
            else:
                answer = True
            
            if answer == False:
                exit()
            else:
                try: 
                    self.client = ccxt.binance({'apiKey': self.api_key,'secret': self.api_secret})
                    #self.client.API_URL = self.api_url #feature version
                                         
                    #state management
                    state = State(config)

                except AuthenticationError as e: #HATAYI döndürüp kontrol edeceğiz.
                    #self.logger.exception(e)
                    pprint(e)
                    exit()
                           
    #wallet yükle, order yükle etc.
    
    def _get_time_offset(self):
        res = self.client.get_server_time()
        return res['serverTime'] - int(time.time() * 1000)

    def synced(self, fn_name, **args):
        args['timestamp'] = int(time.time() - self.time_offset)
        return getattr(self.b, fn_name)(**args)