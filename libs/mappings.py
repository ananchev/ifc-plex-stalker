import libs.logger
logger = libs.logger.logger.getChild('mappings')

class Stalker:    
    database="stalker_db"
    category = {
        'movies' : {'id' : 1, 'alias':'movies'},
        'series' : {'id' : 2, 'alias' : 'tv_shows'}
    }

class Plex:
    moviesSectionID = 2
    tvSectionID = 3
    metaDataCategory = {
        'movies' : 1,
        'series' : 2,
        'seasons' : 3,
        'episodes' : 4}

class Common:
    mappingDict = {
        Plex.moviesSectionID : Stalker.category.get('movies',{}).get('alias'),
        Plex.tvSectionID : Stalker.category.get('series',{}).get('alias')
    }
    @staticmethod
    def getStalkerCategoryAlias(plexSectionID):
        ret = Common.mappingDict.get(plexSectionID)
        if ret:
            return ret
        else:
            logger.error("No mapped Stalker category alias for Plex section ID {}".format(plexSectionID))
            return ret