import os
import sys
import logging as log
from classes.Log import Log

class State():
    
    def __init__(self):
        self.logger = log.getLogger('State')
        pass

    def get_balance(self):
        try:
            balance = client.exchange.fetch_balance(params = {'usdt'})
            print(balance)
        except Exception as e:
            self.logger.exception(e)