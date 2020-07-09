#!/usr/bin/python
from libs.plexdata import PlexData
from libs.logger import logger


def main():
    pd = PlexData(  '/home/ananchev/ifc-plex-stalker',
                    '/home/ananchev/plex-on-sub',
                    '192.168.2.72',
                    'stalker',
                    '1')
    # logger.debug("syncronising Plex genres to Stalker")
    # movies = pd.syncGenres()
    logger.debug("updating ifc_media table with Plex data")
    md = pd.updateIfcMediaTable()
    # logger.debug("updating stalker video table")
    # md = pd.updateStalkerVideoTable()
    

if __name__ == '__main__':
    main()


# fh = logging.FileHandler('spam.log')
# fh.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)
