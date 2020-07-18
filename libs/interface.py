#!/usr/bin/python

from libs.db import DB
from libs.stalker_video import StalkerVideo
from libs.ifc_seasons import IfcSeasons
from libs.ifc_media import IfcMedia
from libs.stalker_seasons import StalkerSeasons
from libs.ifc_episodes import IfcEpisodes
import libs.mappings as mappings

from libs.logger import logger
logger = logger.getChild('interface')

class Interface:

    def __init__(self, app_dir, plex_dir, stalker_db_host,stalker_db_user, stalker_db_pass):        
        dbinst = DB(app_dir,  plex_dir, stalker_db_host, stalker_db_user, stalker_db_pass)
        self.db = dbinst
        self.ifcm = IfcMedia(dbinst)
        self.stvd = StalkerVideo(dbinst)
        self.ifcs = IfcSeasons(dbinst)
        self.stsn = StalkerSeasons(dbinst)
        self.ifep = IfcEpisodes(dbinst)


    def Execute(self):
        logger.info("syncronising Plex genres to Stalker")
        movies = self.stvd.SyncVideoGenres()
        logger.info("updating ifc_media table with Plex data")
        md = self.ifcm.SyncToPlex()
        logger.info("updating stalker video table")
        md = self.stvd.SyncroniseRecords()
        

        logger.info("updating stalker video_season")
        sd = self.ifcs.SyncSeasonData()
        if sd:
            logger.info("syncronising Stalker seasons with data from ifc_tv_seasons")
            ss = self.stsn.SyncStalker()
            logger.info("syncronising episodes data")
            se = self.ifep.SyncEpisodeData()
            pass
        #else:
            #logger.info("No changes or newly added Plex series to sync into Stalker")
            