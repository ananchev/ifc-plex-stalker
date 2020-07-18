#!/usr/bin/python
import datetime

import libs.queries as queries
import libs.mappings as mappings
from libs.interface import Interface

import libs.logger
logger = libs.logger.logger.getChild('stalker_series')

class StalkerSeries:
    "Opreations related to update and sync of video_season & video_season_series tables in Stalker database"

    db = Interface.DB
    


 