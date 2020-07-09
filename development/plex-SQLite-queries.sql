-- media items
SELECT * from media_items WHERE library_section_id = 2 LIMIT 20;
SELECT * from media_items LIMIT 200;
SELECT * from media_items WHERE id = 9755;
SELECT id, metadata_item_id from media_items WHERE library_section_id = 2 LIMIT 10;

SELECT * from metadata_items WHERE library_section_id =2 LIMIT 10;

SELECT * FROM metadata_items LIMIT 10;

--select tags for movies and series
SELECT DISTINCT 
    tags_genre,
    library_section_id
FROM metadata_items
WHERE library_section_id IN (2,3);

--returns the tags
SELECT DISTINCT tags_genre1, tags_genre2 
FROM (
    SELECT DISTINCT 
        tags_genre,
        LENGTH(tags_genre) AS len,
        SUBSTR(tags_genre,1,LENGTH(tags_genre)-(LENGTH(tags_genre)-INSTR(tags_genre, '|')+1))
            AS tags_genre1,
        LTRIM(REPLACE(tags_genre,SUBSTR(tags_genre,1,LENGTH(tags_genre)-(LENGTH(tags_genre)-INSTR(tags_genre, '|')+1)),''),'|')
            AS tags_genre2
    FROM metadata_items
    WHERE library_section_id = 2);

--below is to update the genres in stalker
SELECT DISTINCT tags_genre1 
FROM (
    SELECT DISTINCT 
        tags_genre,
        LENGTH(tags_genre) AS len,
        SUBSTR(tags_genre,1,LENGTH(tags_genre)-(LENGTH(tags_genre)-INSTR(tags_genre, '|')+1))
            AS tags_genre1,
        LTRIM(REPLACE(tags_genre,SUBSTR(tags_genre,1,LENGTH(tags_genre)-(LENGTH(tags_genre)-INSTR(tags_genre, '|')+1)),''),'|')
            AS tags_genre2
    FROM metadata_items
    WHERE library_section_id = 2 AND LENGTH(tags_genre1) > 0)
UNION
SELECT DISTINCT tags_genre2 AS tags_genre1
FROM (
    SELECT DISTINCT 
        tags_genre,
        LENGTH(tags_genre) AS len,
        SUBSTR(tags_genre,1,LENGTH(tags_genre)-(LENGTH(tags_genre)-INSTR(tags_genre, '|')+1))
            AS tags_genre1,
        LTRIM(REPLACE(tags_genre,SUBSTR(tags_genre,1,LENGTH(tags_genre)-(LENGTH(tags_genre)-INSTR(tags_genre, '|')+1)),''),'|')
            AS tags_genre2
    FROM metadata_items
    WHERE library_section_id = 2 AND LENGTH(tags_genre2) > 0);




SELECT 
    media_items.id AS media_id,
    metadata_item_id AS metadata_id,
    CAST(strftime('%s', metadata_items.updated_at) AS INTEGER) AS media_last_update,
    CAST(strftime('%s', media_items.updated_at) AS INTEGER) AS metadata_last_update
FROM media_items
INNER JOIN metadata_items
    ON media_items.metadata_item_id = metadata_items.id
WHERE
    media_items.library_section_id = 2 
    AND
    media_id IN (9415, 9557, 9972, 9695, 9888, 9973, 10135, 10136, 9402, 9407 );



SELECT 
    media_items.id AS media_item_id,
    metadata_item_id AS metadata_item_id,
    hash,
    title, 
    summary,
    (media_items.duration / 1000 / 60) || ' min' AS duration,
    REPLACE(tags_genre,'|',', ') AS tags_genre,
    REPLACE(tags_director,'|',', ') AS tags_director,
    REPLACE(tags_star,'|',', ') AS tags_start,
    year,
    user_thumb_url,
    CAST(strftime('%s', metadata_items.updated_at) AS INTEGER) AS media_last_updated,
    CAST(strftime('%s', media_items.updated_at) AS INTEGER) AS metadata_last_updated
FROM media_items
INNER JOIN metadata_items
    ON media_items.metadata_item_id = metadata_items.id
WHERE
    media_items.library_section_id = 2 
    AND
    media_item_id IN (9415, 9557);

/*
beauty and the beast
id = 9415
metadata_item_id = 10533
*/

/*
band of brothers s1 e1
id=10125
metadata_item_id =10816
*/
SELECT * from metadata_items WHERE id=10816; 
-- id 10816
-- parrent_id 10813
-- guid = com.plexapp.agents.thetvdb://74205/1/1?lang=en
-- metadata_type = 4 /episode in a season
-- hash = 3b63dd86675d6ae476c03eeca153bdd2119a5d9d
-- summary contains the description of the episode
-- no episode posters supported in stalker. Need to parse the series poster
/* band of brothers season1 */
SELECT * from metadata_items WHERE id=10813; 
-- id =10813
-- parrent id 10810
-- guid = com.plexapp.agents.thetvdb://74205/1?lang=en
-- metadata_type = 3 /season in a series
-- hash = 1bea1500d79ff582e1e31088467f448e2b0496e1
-- summary optionally contains the description of the season (empty for BoB)
-- no season posters supported in stalker. Need to parse the series poster
/* band of brothers series */
SELECT * from metadata_items WHERE id=10810; 
---id =10810
-- parrent id NULL
-- guid = com.plexapp.agents.thetvdb://74205?lang=en
-- metadata_type = 2 /series
-- hash = 56e0d25d41f6cde96fed18afd826dccf9285cea0
-- summary contains the series description
-- poster should be parsed from hash and teh user_thumb_url
-- /<plex-lib>/Metadata/TV Shows/<first letter of hash>/<remainder hash>.bundle/Conents/_stored/posters/<filename based on metadata>




/*
little fockers 
id = 9755
metadata_item_id = 10676
*/
SELECT * from metadata_items WHERE library_section_id = 2 AND id=10676; --little fockers
-- id 10533
-- guid = com.plexapp.agents.imdb://tt2771200?lang=en
-- metadata_type = 1 /movies
-- hash = ccd2a9ecc9f846ef2f8d852b81863f30b5c66459
-- /<plex-lib>/Metadata/Movies/<first letter of hash>/<remainder hash>.bundle/Conents/_stored/posters/metadata
-- the movie poster is location can be parsed from thumb_url
-- metadata://posters/com.plexapp.agents.imdb_453436d967b0e75088da037fdd78285032a0e1b9

SELECT DISTINCT tags_genre from metadata_items WHERE metadata_type = 1;

SELECT  title,
        guid,
        summary,
        duration,
        user_thumb_url,
        tags_genre,
        tags_director,
        tags_star,
        year,
        updated_at,
        hash
FROM `metadata_relations` 
WHERE metadata_item_id =10533; 
/*
 relation_type 1 and 5
 =1 (only one record) with related_metadata_item_id = 10534
 =5 (many records) with related_metadata_item_id = 10535
 relation_type 1 used for the trailer

*/

SELECT * from metadata_items WHERE id=10534;
SELECT * from metadata_items WHERE id=10535;

SELECT * FROM `metadata_item_views` 
    WHERE guid = 'com.plexapp.agents.imdb://tt2771200?lang=en' ;


--media streams
SELECT * FROM media_streams WHERE media_item_id = 9415;
/*
    media_item_id 
    stream_type_id (for subtitles = 3)
    url file:///mnt/Video/Movies/Beauty and the Beast (2017)/Beauty and the Beast (2017).bg.srt
    codec (for subtitles values are pgs, ass, srt, mov_text, sub_
    language (bul, eng)
*/

--media parts
SELECT * FROM media_parts WHERE media_item_id = 9415;

--library sections
SELECT * from library_sections LIMIT 10;
SELECT id, name, section_type from library_sections;
/*
#	id	name			section_type
1	1	Music			8
2	2	Movies			1
3	3	TV Shows		2
4	4	Luiza's Videos	1
5	5	Recordings		1
*/

--library locations
SELECT * from section_locations;
/*
#	id	library_section_id	root_path
1	6	1	                /mnt/Music
2	8	2	                /mnt/Video/Movies
3	9	4	                /mnt/Video/Luiza
4	10	3	                /mnt/Video/TV
5	11	5	                /mnt/Video/Recordings
*/