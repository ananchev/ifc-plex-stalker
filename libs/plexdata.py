#!/usr/bin/python
import sqlite3
import pandas as pd
import mysql.connector

import libs.queries as queries
import lib.mappings as mappings

import libs.logger
logger = libs.logger.logger.getChild('plexdata')


class PlexData:
    def __init__(self, app_dir, plex_dir, stalker_db_host,stalker_db_user, stalker_db_pass):
        self.app_dir = app_dir
        logger.debug("Path to this application: " + self.app_dir)
        self.ifc_db_path = app_dir + '/interface.db'
        logger.debug("Using interface db path: " + self.ifc_db_path)
        self.plex_dir = plex_dir
        self.plex_db_path = plex_dir + '/Plug-in Support/Databases/com.plexapp.plugins.library.db'
        logger.debug("Using plex db path: " + self.plex_db_path)
        self.plex_metadata_dir = plex_dir + '/Metadata'
        logger.debug("Using plex metadata folder path: " + self.plex_db_path)
        self.stalker_db_host = stalker_db_host
        self.stalker_db_user = stalker_db_user
        self.stalker_db_pass = stalker_db_pass
        logger.debug("Using stalker database {0} on {1}, connected as {2} user: ".format(mappings.Stalker.database,
                                                                                        self.stalker_db_host,
                                                                                        self.stalker_db_user))
        self.plexDBcon = self.__connect(database="plex")
        self.ifcDBcon = self.__connect(database="ifc")
        self.stalkerDBcon = self.__connect(database="stalker")
    
    def __connect(self, **kw):
        con = None
        try:
            if kw.get('database') == "stalker":
                con = mysql.connector.connect(
                    host=self.stalker_db_host,
                    user=self.stalker_db_user,
                    password=self.stalker_db_pass,
                    database=mappings.Stalker.database
                )
            if kw.get('database') == "plex":
                con = sqlite3.connect(self.plex_db_path)
            if kw.get('database') == "ifc":
                con = sqlite3.connect(self.ifc_db_path)
        except sqlite3.Error as e:
            logger.error("SQLite connection error: %s" % e)
        except mysql.connector.Error as e:
            logger.error("MySQL connection error: %s" % e)
        logger.info("success opening {0} database connection".format(kw.get('database')))
        return con

    def __close_connections(self):
        if self.plexDBcon:
            self.plexDBcon.close()
        if self.ifcDBcon:
            self.ifcDBcon.close()
        if self.stalkerDBcon:
            self.stalkerDBcon.close()
    
    def ___executeSQL(self, query, **kw):
        try:
            data = None
            con = None
            case = 0 #set differently depending on sqlite or mysql db is queried
            if kw.get('database') == "ifc":
                con = self.ifcDBcon
                case = 1 #sqlite db and query
            if kw.get('database') == "plex":
                con = self.plexDBcon
                case = 1
            if kw.get('database') == "stalker":
                con = self.stalkerDBcon
                case = 2
            cur = con.cursor()
            logger.debug("Query to execute:\n\t{0}".format(query))
            cur.execute(query)
            if case == 1:  #sqlite db and query
                data = cur.fetchall()
                if not data:
                    con.commit()
                    logger.debug('{0} rows in {1} database affected by the execute call.'.format(cur.rowcount, kw.get('database')))
                    return True
                logger.debug('{0} rows from {1} database returned.'.format(len(data), kw.get('database')))
            if case == 2:  #mysql db and query
                if cur.description is None:
                # No recordset for INSERT, UPDATE, CREATE, etc
                    logger.debug('No recordset returned by the execute call on {0} database.'.format(kw.get('database')))
                    return True
                else:
                    # Recordset for SELECT
                    data = cur.fetchall()
                    logger.debug('{0} rows from {1} database returned.'.format(cur.rowcount, kw.get('database')))

        except sqlite3.Error as e:
            logger.error("SQLite error: %s" % e)
        except mysql.connector.Error as e:
            logger.error("MySQL  error: %s" % e)
        except Exception as e:
            logger.error("Exception in query: %s" % e)
        return data 
    
    def queryPlex(self, query):
        return self.___executeSQL(query, database ="plex")

    def queryIfcDB(self, query):
        return self.___executeSQL(query, database ="ifc")

    def queryStalker(self, query):
        return self.___executeSQL(query, database ="stalker")

    def pandasReadSQL(self, query, **kw):
        df = None
        con = None
        if kw.get('database') == "ifc":
            con = self.ifcDBcon
        if kw.get('database') == "plex":
            con = self.plexDBcon

        try:
            df = pd.read_sql_query(query,con)
        except Exception as e:
            logger.error("Exception in pandasReadSQL: %s" % e)
        return df 

    def syncGenres(self):
        genres = self.queryPlex(queries.Plex.getCategories)
        genresList = []
        for g in genres:
            categoryAlias = mappings.Common.getStalkerCategoryAlias(g[1])
            if len(g[0]) == 0:
                continue
            if '|' in g[0]:
                genresList.append([categoryAlias, g[0].split('|')[0]])
                genresList.append([categoryAlias, g[0].split('|')[1]])
            else:
                genresList.append([categoryAlias, g[0].split('|')[0]])
        #filter out duplicates
        import itertools
        genresList.sort()
        genresList = list(genresList for genresList, _ in itertools.groupby(genresList))

        for g in genresList:
            updateGenresQuery = queries.Stalker.insertCategoryGenre.format(g[1],g[0])
            self.queryStalker(updateGenresQuery)
        logger.info("Success executing the query to update all {0} TV and Movie genres.".format(len(genresList)))

    def updateIfcMediaTable(self):
        plexMedia = self.queryPlex(queries.Plex.getMediaData)
        ifcPlexMedia = self.queryIfcDB(queries.Ifc.selectPlexMediaData)
        #media_id = [0]
        #metadata_id = [1]
        #media_last_update = [2]
        #metadata_last_update = [3]
        logger.debug("write new plex records")
        for p in plexMedia:
            if not any(im[0] == p[0] for im in ifcPlexMedia): 
                logger.debug("plexMedia_id {} is not present in interface table and will be inserted".format(p[0]))
                updateIfc = queries.Ifc.updatePlexMediaData.format(p[0],p[1],p[2],p[3],1)

        logger.debug("update outdated interface records")
        lst = [t for t in plexMedia if t not in ifcPlexMedia]
        logger.debug("{0} plexMedia_id records in the interface table will be updated:".format(len(lst)))
        for i in lst:
            updateIfc = queries.Ifc.updatePlexMediaData.format(i[0],i[1],i[2],i[3],1)
            self.queryIfcDB(updateIfc)
        logger.debug("mark any records for deletion")
        for i in ifcPlexMedia:
            if not any(pm[0] == i[0] for pm in plexMedia):
                logger.debug("plexMedia_id {} is not present anymore in plex and will be  marked for deleltion".format(i[0]))
                self.queryIfcDB(queries.Ifc.setForDeletion.format(i[0]))

    def updateStalkerVideoTable(self):
        test =1