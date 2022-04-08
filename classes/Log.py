import logging
from rich.logging import RichHandler

class Log:
    def __init__(self):
        logging.basicConfig(handlers=[RichHandler()],
         level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

Log()
