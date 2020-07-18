#!/usr/bin/python
import datetime

import libs.queries as queries
import libs.mappings as mappings
import libs.interface as ifc

import libs.logger
logger = libs.logger.logger.getChild('ifc_episodes')

class IfcEpisodes:
    "Syncronise the interface ifc_tv_episodes table with latest data from Plex"

    def __init__(self, dbisnt):
        self.db = dbisnt

    def SyncEpisodeData(self):
        res = self.WriteEpisodesData()
        if not res: #no seasons to update
            return False #exit sync

    def WriteEpisodesData(self):
        seasons = self.db.queryIfcDB(queries.Ifc.getSeasons)
        nos = len(seasons) if isinstance(seasons, list) else 0
        logger.info("Found {} seasons in ifc_tv_seasons to write or update episodes data for".format(nos))
        if nos == 0:
            return False #no seasons to write episodes for

        #get the existing episodes records in ifc_episodes
        episodesIfc = self.db.queryIfcDB(queries.Ifc.episodesData)

        #for each season record in interface, get the episodes data from Plex
        episodesPlex =[]
        for s in seasons:
            queryP = queries.Plex.getEpisodeData.format(s[0]) 
            episodesInSeason = self.db.queryPlex(queryP)
            for r in episodesInSeason: #collect in the episodes list
                episodesPlex.append((s[0],r[0],r[1])) #tuple (season_metadata_id, episode_media_item_id, episode_number_of_files)

        if isinstance(episodesIfc, bool): #nothing in ifc_episodes table (1st inferface run??)
            logger.info("No episodes records found in ifc_episodes") 
            counter = 0
            for pe in episodesPlex:
                logger.info("episode w. media_item_id={} does not exist in interface table and will be inserted".format(pe[1]))
                insertQuery = queries.Ifc.insertPlexEpisode.format(pe[0],pe[1],pe[2])
                self.db.queryIfcDB(insertQuery)
                counter = counter + 1
            logger.info("{} episodes from Plex inserted in interface table".format(counter))
        else:
            logger.info("Checking for Plex episodes records not in interface table")
            counter = 0
            for pe in episodesPlex:
                if not any(pe[1] == ei[1] for ei in episodesIfc):
                    logger.info("episode w. media_item_id={} does not exist in interface table and will be inserted".format(pe[0]))
                    insertQuery = queries.Ifc.insertPlexEpisode.format(pe[0],pe[1],pe[2])
                    self.db.queryIfcDB(insertQuery)
                    counter = counter +1
            logger.info("{} missing episodes from Plex inserted in interface table".format(counter))

            logger.info("Checking for outdated Plex episodes records in interface table")
            episodesIfc = self.db.queryIfcDB(queries.Ifc.episodesData) #run query again to reflect potential inserts
            counterUpd = 0
            counterDel = 0
            for episode in episodesIfc:
                if not any(episode[0] == plexEpisode[0] for plexEpisode in episodesPlex):
                    logger.info("season_metadata_id {} no longer exists in Plex. All episodes in the interface linked to it will be marked for deletion".format(episode[0]))
                    deleteQuery = queries.Ifc.setEpisodeForDeletion.format("season_metadata_id", episode[0])
                    self.db.queryIfcDB(deleteQuery)
                    counterDel = counterDel + self.db.queryIfcDB(queries.Ifc.countEpisodesInSeason.format(episode[0]))[0][0]
                
                elif not any(episode[1] == plexEpisode[1] for plexEpisode in episodesPlex):
                    logger.info("episode w. media_item_id = {} no longer existis in Plex and will be marked for deletion".format(episode[1]))
                    deleteQuery = queries.Ifc.setEpisodeForDeletion.format("media_item_id", episode[1])
                    self.db.queryIfcDB(deleteQuery)
                    counterDel = counterDel +1

                else: #compare the number of files for the episodes in Plex and Ifc
                    #for every ifc episode, the comprehension below returns the plex episode record that corresponds to the media_item_id
                    i = [pe for pe in episodesPlex if pe[1] == episode[1]][0]
                    if i[2] != episode[2]:
                        logger.info("for episode w. media_item_id {} the # of episode files in Ifc is outdated and will be synced from Plex".format(episode[1]))
                        updateQuery = queries.Ifc.updateEpisodeData.format(i[2],i[1])
                        self.db.queryIfcDB(updateQuery)
                        counterUpd = counterUpd + 1

            logger.info("{} episodes marked for deletion".format(counterDel))
            logger.info("{} episodes updated from Plex".format(counterUpd))   
        return True

    def WriteStalkerSeasonAndVideoIDs(self):
        logger.info("Writing in ifc_episodes the corresponding to every episode Stalker Video ID and Season from ifc_tv_seasons")
