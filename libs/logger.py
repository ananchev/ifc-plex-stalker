import logging
from logging.handlers import RotatingFileHandler
#import logging.config
#logging.config.fileConfig('logging.conf')

logger = logging.getLogger('root')

consoleHandler = logging.StreamHandler()
consoleFormatter = logging.Formatter('%(levelname)s - %(message)s')
consoleHandler.setFormatter(consoleFormatter)

import os, sys
sys.path.insert(1, os.path.realpath(os.path.pardir))
fileHandler = RotatingFileHandler('logfile.log',maxBytes=100000, backupCount=10)
fileFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fileHandler.setFormatter(fileFormatter)

logger.setLevel(logging.DEBUG)
logger.addHandler(consoleHandler)
logger.addHandler(fileHandler)