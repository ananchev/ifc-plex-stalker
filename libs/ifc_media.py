#!/usr/bin/python
import datetime

import libs.queries as queries
import libs.mappings as mappings
import libs.stalker_video as stalker_video

from libs.logger import logger
logger = logger.getChild('ifc_media')


class IfcMedia():   
 
    def __init__(self, dbisnt):
        self.db = dbisnt



    def SyncToPlex(self):
        "syncronise the interface ifc_media table with latest data from Plex"
    
        plexMedia = self.db.queryPlex(queries.Plex.getMediaData)
        ifcPlexMedia = self.db.queryIfcDB(queries.Ifc.allPlexMediaData)
        #media_id = [0]
        #metadata_id = [1]
        #media_last_update = [2]
        #metadata_last_update = [3]
        logger.info("write new plex records")
        nRecords = 0
        for p in plexMedia:
            if not any(im[1] == p[1] for im in ifcPlexMedia): 
                logger.info("plex_metadata_item_id {} is not present in interface table and will be inserted".format(p[1]))
                nRecords = nRecords + 1
                if p[0] is None:
                    updateIfc = queries.Ifc.insertPlexMediaData_series.format(p[1],p[3])
                else:
                    updateIfc = queries.Ifc.insertPlexMediaData_movie.format(p[0],p[1],p[2],p[3])
                self.db.queryIfcDB(updateIfc)
        logger.info("{} new plex records inserted".format(nRecords))

        logger.info("update outdated interface records")

        #rerun query to interface table to reflect potential inserts executed during current run
        ifcPlexMedia = self.db.queryIfcDB(queries.Ifc.allPlexMediaData)
        #find the plex records that are different than what is in the interface table
        lst = [t for t in plexMedia if t not in ifcPlexMedia]

        for i in lst:
            if i[0] is None: #series
                updateIfc = queries.Ifc.updatePlexMediaData_series.format(i[3],i[1])
            else:
                updateIfc = queries.Ifc.updatePlexMediaData_movie.format(i[2],i[3],i[1])
            logger.info("plex_metadata_item_id {} is outdated in interface table and will be synced to Plex".format(i[1]))
            print(str(i))
            print(updateIfc)
            self.db.queryIfcDB(updateIfc)
        logger.info("{0} plex records in the interface table updated".format(len(lst)))

        logger.info("mark any records for deletion")
        dRecords = 0
        for i in ifcPlexMedia:
            if not any(pm[1] == i[1] for pm in plexMedia):
                logger.info("plex_metadata_item_id {} is not present anymore in plex and will be  marked for deleltion".format(i[0]))
                dRecords = dRecords + 1
                self.db.queryIfcDB(queries.Ifc.setMediaForDeletion.format(i[1]))
        logger.info("{} non-exisitng in plex records marked for deletion".format(dRecords))
        self.DeleteMedia()


    @classmethod
    def UpdateInterfaceStalkerRecords(cls, db, recordIDs):
        "writes back the IDs of the new stalker.video records into ifc_media table"

        #get ifc_media data where update flag is 1
        ifcPlexMedia = db.queryIfcDB(queries.Ifc.toWriteStalkerIDs)

        #write stalker video ids against the matching plex metadata_item_ids
        for r in recordIDs:
            if (pm[1] == r[2] for pm in ifcPlexMedia):
                if r[3] in "new":
                    logger.info("writing stalker_video_id {} against plex_metadata_id {}".format(r[0], r[2]))
                else:
                    logger.info("stalker_video_id {} exists against plex_metadata_id {}".format(r[0], r[2]))
                updateQuery = queries.Ifc.updateStalkerVideoID.format(r[0],r[2])
                db.queryIfcDB(updateQuery)
    
    def DeleteMedia(self):
        markedForDelete = self.db.queryIfcDB(queries.Ifc.videoToDeleteInStalker)
        if isinstance(markedForDelete, bool): #no records to delete in Stalker found
            return
        for r in markedForDelete:
            stalker_video.StalkerVideo.DeleteVideo(self.db, r[0])
            logger.info("ifc_media: deleting non exisitng in Plex video with plex_metadata_item_id = {}".format(r[1]))
            self.db.queryIfcDB(queries.Ifc.deleteVideo.format(r[1]))

 



