from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
import logging as log
import modules.menu as menu
import time
import json
from rich import print
from rich.pretty import pprint
from classes.Log import Log

class Binance:
    logger = log.getLogger("Binance")
    
    def __init__(self, config, sync = False):
        self.time_offset = 0
        self.logger.info('Connecting to Binance')
        self.connect(config)

        if sync:
            self.time_offset = self._get_time_offset()

    #Binance connection
    def connect(self, config):
        self.__dict__ = config.exchange
  
        if config.sandbox == True:
            try:
                self.client = Client(self.sandbox_key, self.sandbox_secret)
                self.client.API_URL = self.sandbox_api #sandbox server
                self.logger.info('Connection successful. Sandbox Api')
            except BinanceAPIException as e:
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
                    self.client = Client(self.key, self.secret)
                    #self.client.API_URL = self.api_url #feature version

                    #get status
                    status = self.account_status()
                    
                    if status: 
                        self.logger.info('Connection successful. Trading Api')

                except BinanceAPIException as e: #HATAYI döndürüp kontrol edeceğiz.
                    self.logger.exception(e)
                    exit()
                           
    #wallet yükle, order yükle etc.
    
    def _get_time_offset(self):
        res = self.client.get_server_time()
        return res['serverTime'] - int(time.time() * 1000)

    def synced(self, fn_name, **args):
        args['timestamp'] = int(time.time() - self.time_offset)
        return getattr(self.b, fn_name)(**args)

    def account_status(self):
        return self.client.get_account_status()
