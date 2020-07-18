#!/usr/bin/python
import sqlite3
import mysql.connector
import datetime

import libs.queries as queries
import libs.mappings as mappings

import libs.logger
logger = libs.logger.logger.getChild('db')

class DB:

    def __init__(self, app_dir, plex_dir, stalker_db_host,stalker_db_user, stalker_db_pass):
        self.app_dir = app_dir
        logger.info("Path to this application: " + self.app_dir)
        self.ifc_db_path = app_dir + '/interface.db'
        logger.info("Using interface db path: " + self.ifc_db_path)
        self.plex_dir = plex_dir
        self.plex_db_path = plex_dir + '/Plug-in Support/Databases/com.plexapp.plugins.library.db'
        logger.info("Using plex db path: " + self.plex_db_path)
        self.plex_metadata_dir = plex_dir + '/Metadata'
        logger.info("Using plex metadata folder path: " + self.plex_db_path)
        self.stalker_db_host = stalker_db_host
        self.stalker_db_user = stalker_db_user
        self.stalker_db_pass = stalker_db_pass
        logger.info("Using stalker database {0} on {1}, connected as {2} user: ".format(mappings.Stalker.database,
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
    
    def __executeSQL(self, query, parameters=False, **kw):
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
            if not parameters:
                cur.execute(query)
            else:
                cur.execute(query, parameters)
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
                    con.commit()
                    logger.debug('No recordset returned by the execute call on {0} database.'.format(kw.get('database')))
                    return cur.lastrowid
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
    

    def queryPlex(self, query, parameters=False):
        "run a query against the Plex database"

        if not parameters:
            return self.__executeSQL(query, database ="plex")
        else:
            return self.__executeSQL(query, database ="plex", parameters=parameters)


    def queryIfcDB(self, query, parameters=False):
        "run a query against the interface intermediate database"

        if not parameters:
            return self.__executeSQL(query, database ="ifc")
        else:
            return self.__executeSQL(query, database ="ifc", parameters=parameters)


    def queryStalker(self, query, parameters=False):
        "run a query against the Stalker database"

        if not parameters:
            return self.__executeSQL(query, database ="stalker")
        else:
            return self.__executeSQL(query, database ="stalker", parameters=parameters)
