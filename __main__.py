#!/usr/bin/python
import argparse


from libs.interface import Interface
from libs.logger import logger, dictLoggingOptions

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", 
                        dest='logLevel', 
                        default="INFO", 
                        help="set program logging level",
                        action="store", 
                        choices=["WARNING","INFO", "DEBUG","NOTSET"])
    args = parser.parse_args()
    logger.setLevel(dictLoggingOptions[args.logLevel])

    i = Interface(  '/home/ananchev/ifc-plex-stalker',
                        '/home/ananchev/plex-on-sub',
                        '192.168.2.72',
                        'stalker',
                        '1')
    i.Execute()
    

if __name__ == '__main__':
    main()