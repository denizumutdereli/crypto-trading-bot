import os
import sys
import re
import string
import time
import winsound
from rich.progress import track

def clear():
	os.system('cls' if os.name=='nt' else'clear')

def loading(rangeVal, description):
	for step in track(range(rangeVal), description=description):
			time.sleep(0.1)