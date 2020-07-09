import libs.mappings as mappings
class Plex:
    getCategories="""SELECT DISTINCT tags_genre, library_section_id
    FROM metadata_items
    WHERE library_section_id IN ({}, {});""".format(mappings.Plex.moviesSectionID, 
                                                    mappings.Plex.tvSectionID)

    getMediaData="""SELECT 
        media_items.id AS media_id,
        metadata_item_id AS metadata_id,
        CAST(strftime('%s', metadata_items.updated_at) AS INTEGER) AS media_last_update,
        CAST(strftime('%s', media_items.updated_at) AS INTEGER) AS metadata_last_update
    FROM media_items
    INNER JOIN metadata_items
        ON media_items.metadata_item_id = metadata_items.id
    WHERE
        media_items.library_section_id IN ({}, {}) 
        AND
        media_id IN (9415, 9557, 9972, 9695, 9888, 9973, 10135, 10136, 9402, 9407);""".format(mappings.Plex.moviesSectionID, 
                                                                                        mappings.Plex.tvSectionID)

class Ifc:
    updatePlexMediaData="""REPLACE
        INTO ifc_media(plex_media_id, plex_metadata_item_id, plex_media_last_update, plex_metadata_last_update, ifc_update_stalker)
        VALUES({}, {}, {}, {}, {});"""                                         

    selectPlexMediaData="""SELECT 
        plex_media_id, 
        plex_metadata_item_id, 
        plex_media_last_update, 
        plex_metadata_last_update 
    FROM ifc_media;"""

    setForDeletion="""UPDATE ifc_media 
    SET ifc_for_deletion = 1,
        ifc_update_stalker = 1
    WHERE plex_media_id = {};"""

class Stalker:
    insertCategoryGenre="""INSERT INTO cat_genre (title, category_alias)
    SELECT * FROM (SELECT '{0}', '{1}') AS tmp
    WHERE NOT EXISTS (
        SELECT title FROM cat_genre WHERE title = '{0}'
    ) LIMIT 1"""

class Queries:
    getPlexItems="""
    SELECT 
        media_items.id AS md_id,
        metadata_item_id AS mt_id,
        CAST(strftime('%s', metadata_items.updated_at) AS INTEGER) AS md_lu,
        CAST(strftime('%s', media_items.updated_at) AS INTEGER) AS mt_lu
    FROM media_items
    INNER JOIN metadata_items
        ON media_items.metadata_item_id = metadata_items.id
    WHERE
        media_items.library_section_id = {0} 
        AND
        md_id IN (9415, 9557);"""

    getPlexMediaItems="""
    SELECT 
        media_items.id AS media_item_id,
        metadata_item_id AS metadata_item_id,
        hash,
        title, 
        summary,
        media_items.duration,
        tags_genre,
        tags_director,
        tags_star,
        year,
        user_thumb_url,
        CAST(strftime('%s', metadata_items.updated_at) AS INTEGER) AS media_last_updated,
        CAST(strftime('%s', media_items.updated_at) AS INTEGER) AS metadata_last_updated
    FROM media_items
    INNER JOIN metadata_items
        ON media_items.metadata_item_id = metadata_items.id
    WHERE
        media_items.library_section_id = {0} 
        AND
        media_item_id IN (9415, 9557);"""

    getInterfaceItems="""
    SELECT 
        plex_media_id AS md_id,
        plex_metadata_item_id AS mt_id,
        plex_media_last_update AS md_lu,
        plex_metadata_last_update AS mt_lu
    FROM ifc_media;
    """