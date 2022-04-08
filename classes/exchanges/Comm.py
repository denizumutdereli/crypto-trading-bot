import ccxt
from ccxt import AuthenticationError
import logging as log
import modules.menu as menu
from rich import print
from rich.pretty import pprint
from classes.Log import Log
from classes.State import State

class Comm(State):
    logger = log.getLogger('Exchange')
    
    def __init__(self, config):    
        self.time_offset = 0
        self.connect(config)
 
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
                    self.client = ccxt.binance({'apiKey': self.api_key,'secret': self.api_secret}) #{'nonce': ccxt.Exchange.milliseconds}
                    #self.client.API_URL = self.api_url #feature version

                except AuthenticationError as e: #HATAYI döndürüp kontrol edeceğiz.
                    self.logger.exception(e)
                    exit()