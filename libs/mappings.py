import libs.logger
logger = lib.logger.logger.getChild('mappings')

class Stalker:    
    database="stalker_db"
    moviesCategoryAlias = "movies"
    tvCategoryAlias = "tv_shows"

class Plex:
    moviesSectionID = 2
    tvSectionID = 3

class Common:
    mappingDict = {
        Plex.moviesSectionID : Stalker.moviesCategoryAlias,
        Plex.tvSectionID : Stalker.tvCategoryAlias
    }
    @staticmethod
    def getStalkerCategoryAlias(plexSectionID):
        ret = Common.mappingDict.get(plexSectionID)
        if ret:
            return ret
        else:
            logger.error("No mapped Stalker category alias for Plex section ID {}".format(plexSectionID))
            return ret