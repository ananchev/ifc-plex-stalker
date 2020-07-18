#!/usr/bin/python
import datetime

import libs.queries as queries
import libs.mappings as mappings
import libs.interface as ifc

from libs.logger import logger
logger = logger.getChild('stalker_video')

class StalkerVideo():
    "Opreations related to update and sync of the video table in Stalker database"

    def __init__(self, dbisnt):
        self.db = dbisnt


    def SyncVideoGenres(self):
        "add any new media genres from Plex to Stalker"

        genres = self.db.queryPlex(queries.Plex.getCategories)
        genresList = []
        for g in genres:
            categoryAlias = mappings.Common.getStalkerCategoryAlias(g[1])
            if len(g[0]) == 0:
                continue
            if '|' in g[0]:
                genresList.append((categoryAlias, g[0].split('|')[0]))
                genresList.append((categoryAlias, g[0].split('|')[1]))
            else:
                genresList.append((categoryAlias, g[0].split('|')[0]))

        stalkerGenres = self.db.queryStalker(queries.Stalker.getGenres)
        toAdd = [g for g in genresList if g not in stalkerGenres]

        for g in toAdd:
            self.db.queryStalker(queries.Stalker.insertCategoryGenre, g)
        logger.info("Added {0} TV and Movie genres into Stalker".format(len(toAdd)))


    def SyncroniseRecords(self):
        "executes the sync between ifc_media table and stalker_db"

        #write plex movie & series information into stalker_db.video table
        movVidIDs = self.WriteVideoRecords("movies")     
        serVidIDs = self.WriteVideoRecords("series")
        
        vidIDs = movVidIDs + serVidIDs
        #write back the IDs of the new stalker.video records into ifc_media table
        ifc.IfcMedia.UpdateInterfaceStalkerRecords(self.db, vidIDs)

        #need to run her a Delete both at Stalker and IFC




    def WriteVideoRecords(self, movies_or_series = "movies"):
        "Query Plex and run Stalker update queries"

        recordsIDs=[]
        is_series = 0 if movies_or_series in "movies" else 1

        #get the Plex items not exisiting in Stalker (w/o stalker_video_id in ifc table)
        newPlexData = self.db.queryIfcDB(queries.Ifc.toUpdatePlexMediaData.format(is_series,is_series,''))
        if isinstance(newPlexData, list):  #new moviews or series exist
            logger.info("{} new Plex {} will be added as Stalker videos.".format(len(newPlexData), movies_or_series))
            #query to insert new items into Stalker
            insertQueryStalker = queries.Stalker.insertVideo
            parametersList = self.BuildInsertQueryParams(newPlexData, movies_or_series)
            
            #run the query and collect the new stalker video ids
            recordsIDs = self.UpdateStalkerVideo(insertQueryStalker, parametersList, "new")
        else:
            logger.info("No new Plex {} to add into Stalker videos table.".format(movies_or_series))  

        #get the existing Plex items where update is needed
        toUpdatePlexData = self.db.queryIfcDB(queries.Ifc.toUpdatePlexMediaData.format(is_series,is_series,'NOT'))
        if isinstance(toUpdatePlexData, list):
            logger.info("{} Plex {} will be updated into Stalker.".format(len(toUpdatePlexData), movies_or_series))

            #query to update the Stalker records
            updateQueryStalker = queries.Stalker.updateVideo
            parametersList = self.BuildInsertQueryParams(toUpdatePlexData, movies_or_series)
            
            #run the query and collect the updated stalker video ids
            recordsIDs = recordsIDs + self.UpdateStalkerVideo(updateQueryStalker, parametersList, "update")

        else:
            logger.info("No Plex {} to update into Stalker videos table.".format(movies_or_series))  
        
        return recordsIDs



    def UpdateStalkerVideo(self, query, parametersList, new_or_update):
        "inserts or updates a line / video in stalker_db.video"

        retval = []
        for p in parametersList:
            if new_or_update in "new":
                r = self.db.queryStalker(query, p[0])
                retval.append([r, p[1], p[2], new_or_update])
            else:
                #for updates first query the interface table to find stalker_db.video.id
                stalkerID = self.db.queryIfcDB(queries.Ifc.stalkerID.format(p[2]))[0][0]
                #then pass to the stalker update query so the record to update can be located
                r = self.db.queryStalker(query.format(stalkerID), p[0])
                retval.append([stalkerID, p[1], p[2], new_or_update])      
        return retval



    def BuildInsertQueryParams(self, plexData, movies_or_series):
        "Traverse results of plex data query and return as parameters tuple to insert/update video record into Stalker"

        retval = []

        stalkerCatAlias = mappings.Stalker.category.get(movies_or_series,{}).get('alias')
        is_series = 1 if movies_or_series in 'series' else 0
        query = queries.Plex.getSeriesData if movies_or_series in 'series' else queries.Plex.getMovieData

        for d in plexData:
            #get Plex meta-data required for Stalker video table
            metadatCatID = mappings.Plex.metaDataCategory[movies_or_series]
            videoData = self.db.queryPlex(query.format(metadatCatID, d[1]))
            #split the common genres field from plex into four genres tags for Stalker
            genres = videoData[0][5].split('|') #query only returns one row - hence the first [0] index
            genres.extend([""]*(4-len(genres))) #extend the list with empty spaces to cover all 4 stalker categories
            for g in genres:
                if g:
                    id = self.db.queryStalker(queries.Stalker.getCatGenreID.format(stalkerCatAlias, g))
                pass
            genre_ids = [self.db.queryStalker(queries.Stalker.getCatGenreID.format(stalkerCatAlias, g))[0][0] if g else '' for g in genres]
            query_params=(videoData[0][0],   #name
                        videoData[0][1],     #o_name
                        videoData[0][2],     #time
                        videoData[0][3],     #description
                        videoData[0][0].replace(" ", "_") + "_" + str(videoData[0][8]),     #path
                        videoData[0][4],     #category_id
                        genre_ids[0],        #cat_genre_id_1
                        genre_ids[1],        #cat_genre_id_2
                        genre_ids[2],        #cat_genre_id_3
                        genre_ids[3],        #cat_genre_id_4
                        videoData[0][6],     #director
                        videoData[0][7],     #actors
                        videoData[0][8],     #year
                        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  #added
                        " ",                 #protocol
                        1,                   #accessed
                        1,                   #status
                        1,                   #admin_id
                        is_series,)          #is_series
            retval.append ([query_params,d[0],d[1]]) #(query params tuple, plex media id, plex metadata id)
        return retval

    @classmethod
    def DeleteVideo(cls,db,stalker_video_id):
        logger.info("stalker_db.video: deleting non-existing in Plex video with stalker ID = {}".format(stalker_video_id))
        db.queryStalker(queries.Stalker.deleteVideo.format(stalker_video_id))





