import os
import sys

class Settings:
   
    def __init__(self,verbose):
        self.root = os.path.dirname(os.path.realpath(__file__)) + '/../' #system,
        self.sounds =  0 #sounds on - of
        if verbose:
            self.verbose = True
        pass