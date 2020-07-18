ATTACH '/home/ananchev/plex-on-sub/Plug-in Support/Databases/com.plexapp.plugins.library.db'
    AS pdb;
ATTACH '/home/ananchev/ifc-plex-stalker/interface.db'
    AS idb;

SELECT 
    plex_media_id AS ifc_plex_media_id,
    plex_metadata_item_id AS ifc_plex_metadata_item_id,
    plex_media_last_update AS ifc_plex_media_last_update,
    plex_metadata_last_update AS ifc_plex_metadata_last_update
FROM ifc_media;

SELECT
    plex_metadata_item_id
FROM ifc_media
WHERE
    is_series = 1
    AND
    ifc_update_stalker = 1
    AND
    ifc_for_deletion = 0;

SELECT
    series_metadata_id,
    season_metadata_id
FROM ifc_tv_seasons

FROM ifc_media;
DELETE FROM ifc_media WHERE plex_metadata_item_id = 11511;

SELECT plex_media_id FROM ifc_media;

-- --below are new  
-- 9402 10524 1593469852 1535123783
-- 9407 10529 1593469828 1536082969
-- 10810


-- --below two are real untouched
-- REPLACE
-- INTO ifc_media(plex_media_id, plex_metadata_item_id,plex_media_last_update,plex_metadata_last_update)
-- VALUES(9415, 10533, 1593469440, 1536430128);
-- REPLACE
-- INTO ifc_media(plex_media_id, plex_metadata_item_id,plex_media_last_update,plex_metadata_last_update)
-- VALUES(9557, 10585, 1593469428, 1536534315);

-- --below two will be with wrong plex_media_last_update
-- --correct plex_media_last_update for 10755 = 1546374845, and for 10637 = 1537104922
-- UPDATE ifc_media SET plex_media_last_update = 1593469222 WHERE plex_metadata_item_id = 10755
-- UPDATE ifc_media SET plex_media_last_update = 1593469222 WHERE plex_metadata_item_id = 10637

--UPDATE ifc_media SET ifc_update_stalker = 0 WHERE plex_metadata_item_id = 10637
--UPDATE ifc_media SET ifc_update_stalker = 0 WHERE plex_metadata_item_id = 10755

-- DELETE FROM ifc_media WHERE plex_metadata_item_id = 10755
-- DELETE FROM ifc_media WHERE plex_metadata_item_id = 10637


-- --below two will be with wrong plex_metadata_last_update
-- --correct plex_metadata_last_update for 9888 = 1546256610, and for 9973 = 1546639968
-- UPDATE ifc_media SET plex_metadata_last_update = 1546256555 WHERE plex_metadata_item_id = 10725
-- UPDATE ifc_media SET plex_metadata_last_update = 1546639333 WHERE plex_metadata_item_id = 10756
-- DELETE FROM ifc_media WHERE plex_metadata_item_id = 10725
-- DELETE FROM ifc_media WHERE plex_metadata_item_id = 10756
-- DELETE FROM ifc_media WHERE plex_metadata_item_id = 11117


-- --below two will be with wrong both and plex_media_last_update and plex_metadata_last_update 
-- --correct plex_media_last_update for 10824 = 1593469469, and for 10824 = 1593469516
-- --correct plex_metadata_last_update for 10825 = 1556921126, and for 10825 = 1556921835
-- UPDATE ifc_media SET plex_metadata_last_update = 1546256556, plex_media_last_update = 1593469444 WHERE plex_metadata_item_id = 10824
-- UPDATE ifc_media SET plex_metadata_last_update = 1546639777, plex_media_last_update = 1593469666 WHERE plex_metadata_item_id = 10825


-- -- below are missing in plex
-- REPLACE
-- INTO ifc_media(plex_media_id, plex_metadata_item_id,plex_media_last_update,plex_metadata_last_update)
-- VALUES(2222, 113411, 1536430189, 1536430189);
-- REPLACE
-- INTO ifc_media(plex_media_id, plex_metadata_item_id,plex_media_last_update,plex_metadata_last_update)
-- VALUES(3333, 11891, 1536430189, 1536430189);

-- DELETE FROM ifc_media where stalker_video_id = 321
--DELETE FROM ifc_tv_seasons
--UPDATE ifc_media SET updt_seas = 1 WHERE is_series = 1
--WHERE plex_media_id = ;

-- UPDATE ifc_media SET stalker_video_id = NULL;
-- UPDATE ifc_media SET updt_series = NULL;
-- UPDATE ifc_media SET updt_seas = 0 WHERE is_series=1


-- UPDATE ifc_tv_seasons SET stalker_season_id = NULL;
-- DELETE from ifc_media where plex_metadata_item_id = 10810;
-- DELETE from ifc_tv_seasons where season_metadata_id = 10813;
-- DELETE from ifc_tv_seasons where series_metadata_id = 11511;
-- UPDATE ifc_tv_seasons SET metadata_last_update = 1234, nbr_episodes=8  WHERE season_metadata_id = 11512;

-- SELECT im.stalker_video_id, it.series_metadata_id
--     FROM ifc_media AS im
-- JOIN ifc_tv_seasons AS it
-- ON im.plex_metadata_item_id = it.series_metadata_id
-- WHERE it.updt_seas = 1
--     AND
--     it.for_deletion = 0

-- INSERT INTO ifc_tv_seasons (series_metadata_id, season_metadata_id, season_index, nbr_episodes, metadata_last_update, stalker_video_id, stalker_season_id)
-- VALUES (55555, 6666, 1, 99, 3333333, 5000, 6000)

SELECT COUNT(*) as count
FROM ifc_tv_seasons
WHERE series_metadata_id = 100000

---SELECT * FROM ifc_tv_seasons;
-- SELECT * FROM ifc_media;
-- SELECT * FROM ifc_episodes;

-- DELETE FROM ifc_media WHERE stalker_video_id = 299

-- REPLACE
-- INTO ifc_tv_seasons(season_metadata_id)
-- VALUES(1);

SELECT
        season_metadata_id,
        stalker_video_id
    FROM ifc_tv_seasons
    WHERE for_deletion = 0;

SELECT 
        stalker_season_id,
        season_metadata_id
    WHERE 
        for_deletion = 1
        AND
        ifc_update_stalker = 1;

SELECT DISTINCT ie.media_item_id, it.stalker_video_id, it.stalker_season_id
    FROM ifc_tv_seasons AS it
    JOIN ifc_episodes AS ie
        ON ie.season_metadata_id = it.season_metadata_id
    WHERE 
        ie.updt_episodes = 1 