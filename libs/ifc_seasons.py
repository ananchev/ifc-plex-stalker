#!/usr/bin/python
import datetime

import libs.queries as queries
import libs.mappings as mappings
import libs.interface as ifc
import libs.stalker_seasons as ss

import libs.logger
logger = libs.logger.logger.getChild('ifc_seasons')

class IfcSeasons:
    "Syncronise the interface ifc_tv_seasons table with latest data from Plex"

    def __init__(self, dbisnt):
        self.db = dbisnt

    def SyncSeasonData(self):
        res = self.WriteSeasonRecords()
        if not res: #no series to update
            return False #exit season sync
        self.WriteStalkerVideoIDs()
        self.DeleteSeasons()
        return res

    def WriteSeasonRecords(self):
        series = self.db.queryIfcDB(queries.Ifc.selectSeasonData) #get all series data from interface media
        noS = len(series) if not isinstance(series, bool) else 0 #no series exist in ifc_media table
        logger.info("Found {} records in ifc_media with series data to process.".format(noS)) 
        if noS == 0:
            return False #exit function

        #get the existing season data in ifc_tv_seasons
        queryI = queries.Ifc.seasonsData
        sDataIfc = self.db.queryIfcDB(queryI)

        #for each series record in interface (already synced to plex), get the seasons from plex 
        sDataPlex = []
        for s in series: 
            queryP = queries.Plex.getSeasonData.format(s[0])
            seasonsInSeries = self.db.queryPlex(queryP)
            for r in seasonsInSeries:
                sDataPlex.append(r) #collect in seasons data list
        
        if isinstance(sDataIfc, bool): #nothing in interface table (perhaps 1st interface run)
            logger.info("No series seasons records found in ifc_tv_seasons") 
            counter = 0
            for plexSerie in sDataPlex:
                logger.info("season_metadata_id {} is not present in interface series table and will be inserted".format(plexSerie[3]))
                insertQuery = queries.Ifc.insertPlexSeriesSeason.format(plexSerie[0],plexSerie[3],plexSerie[4],plexSerie[2],plexSerie[5])
                self.db.queryIfcDB(insertQuery)
                counter = counter + 1
            logger.info("{} Plex series records inserted in interface table".format(counter))
        else: 
            logger.info("Checking for new Plex series records not in interface table")
            counter = 0
            for plexSerie in sDataPlex:
                if not any(plexSerie[3] == ifcSerie[1] for ifcSerie in sDataIfc):
                    logger.info("season_metadata_id {} is not present in interface series table and will be inserted".format(plexSerie[3]))
                    insertQuery = queries.Ifc.insertPlexSeriesSeason.format(plexSerie[0],plexSerie[3],plexSerie[4],plexSerie[2],plexSerie[5])
                    self.db.queryIfcDB(insertQuery)
                    counter = counter + 1
            logger.info("{} missing Plex series records inserted in interface table".format(counter))

            logger.info("Checking for outdated Plex series records in interface table")
            sDataIfc = self.db.queryIfcDB(queryI) #run query again to reflect potential inserts
            counterDel = 0
            counterUpd = 0
            for seasonInIfc in sDataIfc:
                if not any(seasonInIfc[0] == seasonInPlex[0] for seasonInPlex in sDataPlex): #compares series_metadata_id
                    logger.info("series_metadata_id {} no longer exists in Plex. All seasons in the interface linked to it will be marked for deletion".format(seasonInIfc[0]))
                    deleteQuery = queries.Ifc.setSeasonForDeletion.format("series_metadata_id", seasonInIfc[0])
                    self.db.queryIfcDB(deleteQuery)
                    counterDel = counterDel + self.db.queryIfcDB(queries.Ifc.countSeasonsInSeries.format(seasonInIfc[0]))[0][0]
                    
                elif not any(seasonInIfc[1] == seasonInPlex[3] for seasonInPlex in sDataPlex): #compares season_metadata_id
                    logger.info("season_metadata_id {} no longer exists in Plex and will be marked for deletion".format(seasonInIfc[1]))
                    deleteQuery = queries.Ifc.setSeasonForDeletion.format("season_metadata_id", seasonInIfc[1])
                    self.db.queryIfcDB(deleteQuery)
                    counterDel = counterDel + 1
                else: #Compare the season series number in plex and ifc
                    p = [sdp for sdp in sDataPlex if sdp[3] == seasonInIfc[1]][0]
                    if p[5] != seasonInIfc[3] :
                        logger.info("for season_metadata_id {} the # of episodes in Ifc is outdate and will be syncet from Plex".format(seasonInIfc[1]))
                        updateQuery = queries.Ifc.updatePlexSeasonData.format(p[4],p[2],p[5],p[3])

                        self.db.queryIfcDB(updateQuery)
                        counterUpd = counterUpd + 1
            logger.info("{} seasons marked for deletion".format(counterDel))
            logger.info("{} seasons updated from Plex".format(counterUpd))
        return True

    def WriteStalkerVideoIDs(self):
        logger.info("Updating stalker Video ID from ifc_media to ifc_tv_seasons")
        ids = self.db.queryIfcDB(queries.Ifc.stalkerVideoIDtoPlexSeriesId)
        if isinstance(ids, bool):
            no = 0
            logger.info("No series seasons for which to copy stalker Video ID")
        else:
            no = len(ids)
            for item in ids:
                logger.info("Writing Stalker Video ID {} to series_metadata_id {}".format(item[0], item[1]))
                query = queries.Ifc.writeStalkerVideoIDtoSeason.format(item[0],item[1])
                self.db.queryIfcDB(query)
    
    @classmethod
    def WriteStalkerSeasonIDs(cls, db, records_type,ids):
        for t in ids:
            if records_type in "new":
                logger.info("Writing stalker_season_id {} against season_metadata_id {}".format(t[0],t[1]))
                query = queries.Ifc.writeStalkerSeasonIDs.format(t[0],t[1])
            else:
                logger.info("Clearing updt_seas for season_metadata_id {}".format(t[1]))
                query = queries.Ifc.muteUpdtSeasFlagInIfcSeasons.format(t[1])
            db.queryIfcDB(query)

    def DeleteSeasons(self):
        markedForDelete = self.db.queryIfcDB(queries.Ifc.seasonsToDeleteInStalker)
        if isinstance(markedForDelete, bool): #no records to delete in Stalker found
            return
        for r in markedForDelete:
            ss.StalkerSeasons.DeleteNonExistingSeason(self.db,r[0])
            logger.info("ifc_tv_seasons: deleting non exisitng in Plex season with season_metadata_id = {}".format(r[1]))
            self.db.queryIfcDB(queries.Ifc.deleteSeason.format(r[1]))

 