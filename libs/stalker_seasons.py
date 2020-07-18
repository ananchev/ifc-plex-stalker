#!/usr/bin/python
import datetime

import libs.queries as queries
import libs.mappings as mappings
import libs.interface as ifc

import libs.logger
logger = libs.logger.logger.getChild('stalker_seasons')

class StalkerSeasons:
    "Opreations related to update and sync of the video_season table in Stalker database"

    def __init__(self, dbisnt):
        self.db = dbisnt

    def SyncStalker(self):
        modIDs = self.WriteToStalker()
        new = [r for r in modIDs if r[2] in "new"]
        updt = [r for r in modIDs if r[2] in "updated"]
        if isinstance(new, list):
            logger.info("Writing back {} stalker_season_id records into ifc_tv_seasons".format(len(new)))
            ifc.IfcSeasons.WriteStalkerSeasonIDs(self.db, "new" ,new)
        if isinstance(updt, list):
            logger.info("Set as update completed for {} stalker_season_id records in ifc_tv_seasons".format(len(updt)))
            ifc.IfcSeasons.WriteStalkerSeasonIDs(self.db, "updated", updt)
        if len(modIDs) == 0:
            logger.info("No new records inserted in stalker_db.video_season")

    def WriteToStalker(self):
        "Updates stalker_db.video_season table with data from the interface"
        ifcRecords = self.db.queryIfcDB(queries.Ifc.toWriteinStalkerVideoSeason)
        if isinstance(ifcRecords, bool):
            logger.info("no ifc_tv_seasons to write or update in Stalker")
            return []
        new = [r for r in ifcRecords if r[0] == None]
        updt = [r for r in ifcRecords if r[0] != None]
        modIDs = []
        if isinstance(new, list):
            logger.info("{} ifc_tv_seasons new records will be written in Stalker".format(len(new)))
            insertQuery = queries.Stalker.insertSeason
            for r in new:
                params = (
                    r[1], #stalker_video_id 
                    r[2], #season_index
                    r[3], #season_name
                    r[4], #nbr_episodes
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), #date_add
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #date_modify
                )
                sId = self.db.queryStalker(insertQuery,params)
                modIDs.append((sId, r[5],"new")) #tuple stalker_season_id, season_metadata_id - use to update ifc_tv_seasons 
        if isinstance(updt, list):
            logger.info("{} ifc_tv_seasons records will be updated in Stalker".format(len(updt)))    
            for r in updt:
                updateQuery = queries.Stalker.updateSeason.format(r[0])
                params = (
                    r[4], #nbr_episodes
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #date_modify
                )
                sId = self.db.queryStalker(updateQuery,params)
                modIDs.append((r[0],r[5],"updated"))
        return modIDs

    @classmethod
    def DeleteNonExistingSeason(cls, db, video_season_id):
        logger.info("stalker_db.video_season: deleting non-existing in Plex  season with stalker ID = {}".format(video_season_id))
        db.queryStalker(queries.Stalker.deleteSeriesSeason.format(video_season_id))
