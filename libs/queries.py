import libs.mappings as mappings
class Plex:
    getCategories="""SELECT DISTINCT tags_genre, library_section_id
    FROM metadata_items
    WHERE library_section_id IN ({}, {});""".format(mappings.Plex.moviesSectionID, 
                                                    mappings.Plex.tvSectionID)

    getMediaData="""SELECT 
        media_items.id AS media_id,
        metadata_items.id AS metadata_id,
        CAST(strftime('%s', media_items.updated_at) AS INTEGER) AS media_last_update,
        CAST(strftime('%s', metadata_items.updated_at) AS INTEGER) AS metadata_last_update,
        CASE metadata_items.metadata_type
            WHEN 2 THEN 1
            WHEN 1 THEN 0
        END AS is_series
    FROM metadata_items
    LEFT JOIN media_items
        ON (metadata_items.id = media_items.metadata_item_id)
    WHERE
        metadata_items.library_section_id IN ({}, {})
        AND
        metadata_items.metadata_type IN (1,2)
        AND
        metadata_items.id IN (10533, 10585, 10755, 10637, 10725, 10756, 10824, 10825, 10524, 10529, 11117, 10810 );""".format(mappings.Plex.moviesSectionID, 
                                                                                        mappings.Plex.tvSectionID)
        #11511 the good fight
        #10810 band of brothers
    getMovieData="""SELECT 
        title as name,
        title as o_name,
        (media_items.duration / 1000 / 60) AS time,
        summary as description,
        {} as category_id,    
        tags_genre AS category_genre_tags,
        REPLACE(tags_director, '|',', ') AS director,
        REPLACE(tags_star, '|',', ') AS actors,
        year,
        metadata_type
    FROM media_items
    INNER JOIN metadata_items
        ON media_items.metadata_item_id = metadata_items.id
    WHERE
        metadata_items.id = {};"""

    getSeriesData="""
    SELECT 
        title as name,
        title as o_name,
        '' AS time,
        summary as description,
        {} as category_id,    
        tags_genre AS category_genre_tags,
        REPLACE(tags_director, '|',', ') AS director,
        REPLACE(tags_star, '|',', ') AS actors,
        year,
        metadata_type
    FROM metadata_items
    WHERE
        metadata_items.id = {};"""
    
    getSeasonData="""SELECT 
        mi.parent_id as series_metadata_id,
        metadata_season.title as series_title,
        mi.'index' as season,
        mi.id as season_metadata_id,
        CAST(strftime('%s', metadata_season.updated_at) AS INTEGER) AS s_metadata_last_updated,
        COUNT(*) as nbr_episodes
    FROM metadata_items as mi
    JOIN metadata_items AS metadata_season 
        ON mi.parent_id = metadata_season.id
    LEFT OUTER JOIN metadata_items as metadata_episodes
        ON mi.id = metadata_episodes.parent_id
    WHERE mi.parent_id ={}
    GROUP BY season_metadata_id
    """

    getEpisodeData = """SELECT 
        mi.id as media_item_id,
        COUNT(*) AS number_of_files
    FROM metadata_items AS mti
    JOIN media_items AS mi
        ON mi.metadata_item_id = mti.id
    JOIN media_streams AS ms
        ON ms.media_item_id = mi.id
    WHERE 
        mti.parent_id = {}
        AND 
        ms.stream_type_id IN (1, 3) --1=video, 3=subs
    GROUP BY ms.media_item_id;"""

class Ifc:
    insertPlexMediaData_movie="""REPLACE
        INTO ifc_media(plex_media_id, plex_metadata_item_id, plex_media_last_update, plex_metadata_last_update, ifc_update_stalker, updt_video, updt_files, updt_seas)
        VALUES({}, {}, {}, {}, 1, 1, 1, NULL);"""

    insertPlexMediaData_series= """REPLACE
        INTO ifc_media(plex_metadata_item_id, plex_metadata_last_update, ifc_update_stalker, is_series, updt_video, updt_seas, updt_files)
        VALUES({}, {}, 1, 1, 1, 1, 1);"""

    insertPlexSeriesSeason="""INSERT 
    INTO ifc_tv_seasons(series_metadata_id, season_metadata_id, metadata_last_update, season_index ,nbr_episodes, ifc_update_stalker, updt_seas, updt_episodes)
    VALUES({}, {}, {}, {}, {}, 1 , 1, 1);"""

    insertPlexEpisode="""INSERT
    INTO ifc_episodes(season_metadata_id, media_item_id, number_of_files, ifc_update_stalker, updt_episodes)
    VALUES({},{},{},1,1)
    """

    updatePlexMediaData_movie="""UPDATE ifc_media 
        SET 
            plex_media_last_update = {},
            plex_metadata_last_update = {},
            ifc_update_stalker = 1,
            updt_video = 1,
            updt_files= 1
        WHERE plex_metadata_item_id = {}"""
    
    updatePlexMediaData_series="""UPDATE ifc_media 
        SET 
            plex_metadata_last_update = {},
            ifc_update_stalker = 1, 
            updt_video = 1,
            updt_files= 1, 
            updt_seas = 1
        WHERE plex_metadata_item_id = {}"""

    updatePlexSeasonData="""UPDATE ifc_tv_seasons
        SET 
            metadata_last_update = {},
            season_index = {},
            nbr_episodes = {},
            ifc_update_stalker = 1,
            updt_seas = 1,
            updt_episodes = 1
        WHERE season_metadata_id = {}"""
    
    updateEpisodeData="""UPDATE ifc_episodes
    SET 
        number_of_files = {},
        ifc_update_stalker = 1,
        updt_episodes = 1
    WHERE media_item_id = {}"""

    updateStalkerVideoID="""UPDATE ifc_media
        SET stalker_video_id = {}, 
            updt_video = 0
        WHERE plex_metadata_item_id = {};"""    

    allPlexMediaData="""SELECT 
        plex_media_id, 
        plex_metadata_item_id,
        plex_media_last_update,
        plex_metadata_last_update,
        is_series
    FROM ifc_media;"""

    toWriteinStalkerVideoSeason="""SELECT
        stalker_season_id,
        stalker_video_id,
        season_index,
        "Season " || season_index AS season_name,
        nbr_episodes,
        season_metadata_id
    FROM ifc_tv_seasons
    WHERE 
        updt_seas = 1
        AND
        for_deletion = 0;"""




    toUpdatePlexMediaData="""SELECT 
        plex_media_id, 
        plex_metadata_item_id
    FROM ifc_media
    WHERE 
        ifc_for_deletion = 0
        AND
        updt_video = 1
        AND
        is_series IN ({}, {})
        AND
        stalker_video_id IS {} NULL;"""

    toWriteStalkerIDs="""SELECT 
        plex_media_id, 
        plex_metadata_item_id
    FROM ifc_media
    WHERE 
        ifc_for_deletion = 0
        AND
        updt_video = 1;"""

    setMediaForDeletion="""UPDATE ifc_media 
    SET ifc_for_deletion = 1,
        ifc_update_stalker = 1
    WHERE plex_metadata_item_id = {};"""

    setSeasonForDeletion="""UPDATE ifc_tv_seasons 
    SET for_deletion = 1,
        ifc_update_stalker = 1
    WHERE {} = {};"""

    setEpisodeForDeletion="""UPDATE ifc_episodes 
    SET for_deletion = 1,
        ifc_update_stalker = 1
    WHERE {} = {};"""

    stalkerID="""SELECT stalker_video_id
    FROM ifc_media 
    WHERE plex_metadata_item_id = {};"""

    selectSeasonData="""SELECT
        plex_metadata_item_id
    FROM ifc_media
    WHERE
        ifc_for_deletion = 0
        AND
        is_series = 1;"""

    getSeasons="""SELECT
        season_metadata_id,
        stalker_video_id
    FROM ifc_tv_seasons
    WHERE for_deletion = 0;"""

    seasonsData="""SELECT
        series_metadata_id,
        season_metadata_id,
        metadata_last_update,
        nbr_episodes
    FROM ifc_tv_seasons;"""

    episodesData="""SELECT
        season_metadata_id,
        media_item_id,
        number_of_files
    FROM ifc_episodes;"""

    writeStalkerSeasonIDs="""UPDATE ifc_tv_seasons
    SET 
        stalker_season_id ={},
        updt_seas = 0
    WHERE season_metadata_id = {}
    """

    muteUpdtSeasFlagInIfcSeasons="""UPDATE ifc_tv_seasons
    SET
        updt_seas = 0
    WHERE season_metadata_id = {}"""

    countSeasonsInSeries="""SELECT COUNT(*) as count
    FROM ifc_tv_seasons
    WHERE series_metadata_id = {};"""

    countEpisodesInSeason="""SELECT COUNT(*) as count
    FROM ifc_episodes
    WHERE season_metadata_id = {};"""

    stalkerVideoIDtoPlexSeriesId="""SELECT DISTINCT im.stalker_video_id, it.series_metadata_id
    FROM ifc_media AS im
    JOIN ifc_tv_seasons AS it
        ON im.plex_metadata_item_id = it.series_metadata_id
    WHERE 
        it.updt_seas = 1 
        AND
        it.stalker_video_id IS NULL;"""

    stalkerSeasonAndVideoIDsToPlexEpisode="""SELECT DISTINCT im.stalker_video_id, it.series_metadata_id
    FROM ifc_media AS im
    JOIN ifc_tv_seasons AS it
        ON im.plex_metadata_item_id = it.series_metadata_id
    WHERE 
        it.updt_seas = 1 
        AND
        it.stalker_video_id IS NULL;"""

    writeStalkerVideoIDtoSeason="""UPDATE ifc_tv_seasons
    SET stalker_video_id = {}
    WHERE series_metadata_id ={};"""

    videoToDeleteInStalker="""SELECT
        stalker_video_id,
        plex_metadata_item_id
    FROM ifc_media
    WHERE
        ifc_for_deletion = 1;"""

    seasonsToDeleteInStalker="""SELECT 
        stalker_season_id,
        season_metadata_id
    FROM ifc_tv_seasons
    WHERE 
        for_deletion = 1;"""
    
    deleteVideo="""DELETE FROM ifc_media
    WHERE plex_metadata_item_id = {}"""
    
    
    deleteSeason="""DELETE FROM ifc_tv_seasons
    WHERE season_metadata_id = {}"""

class Stalker:
    getCatGenreID="""SELECT id
    FROM cat_genre
    WHERE 
        category_alias = '{}'
        AND
        title = '{}'"""

    getGenres="""SELECT category_alias, title
    FROM cat_genre"""

    insertCategoryGenre="""INSERT INTO cat_genre (category_alias, title)
    VALUES (%s, %s)"""

    insertVideo="""INSERT INTO video (
                                    name, 
                                    o_name, 
                                    time, 
                                    description, 
                                    path,
                                    category_id, 
                                    cat_genre_id_1,
                                    cat_genre_id_2,
                                    cat_genre_id_3,
                                    cat_genre_id_4,
                                    director,
                                    actors,
                                    year,
                                    added,
                                    protocol,
                                    accessed,
                                    status,
                                    admin_id,
                                    is_series
                                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    updateVideo="""UPDATE video
                    SET name = %s, 
                        o_name = %s, 
                        time = %s, 
                        description = %s, 
                        path = %s,
                        category_id = %s, 
                        cat_genre_id_1 = %s,
                        cat_genre_id_2 = %s,
                        cat_genre_id_3 = %s,
                        cat_genre_id_4 = %s,
                        director = %s,
                        actors = %s,
                        year = %s,
                        added = %s,
                        protocol = %s,
                        accessed = %s,
                        status = %s,
                        admin_id = %s,
                        is_series = %s
                    WHERE id = {}"""

    insertSeason = """INSERT INTO video_season (
        video_id,
        season_number,
        season_name,
        season_series,
        date_add,
        date_modify
        )
    VALUES(%s, %s, %s, %s, %s, %s)"""

    updateSeason = """UPDATE video_season
    SET season_series = %s,
        date_modify = %s
    WHERE id = {}"""

    deleteVideo = """DELETE FROM video
    WHERE id ={}"""

    deleteSeriesSeason = """DELETE FROM video_season
    WHERE id ={}"""