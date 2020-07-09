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

SELECT * FROM ifc_media;

SELECT plex_media_id FROM ifc_media;

--below are new  
9402 10524 1593469852 1535123783
9407 10529 1593469828 1536082969
DELETE FROM ifc_media
WHERE plex_media_id IN (9402,9407);

--below two are real untouched
REPLACE
INTO ifc_media(plex_media_id, plex_metadata_item_id,plex_media_last_update,plex_metadata_last_update)
VALUES(9415, 10533, 1593469440, 1536430128);
REPLACE
INTO ifc_media(plex_media_id, plex_metadata_item_id,plex_media_last_update,plex_metadata_last_update)
VALUES(9557, 10585, 1593469428, 1536534315);

--below two will be with wrong plex_media_last_update
--correct plex_media_last_update for 9972 = 1593469475, and for 9695 = 1593469843
REPLACE
INTO ifc_media(plex_media_id, plex_metadata_item_id,plex_media_last_update,plex_metadata_last_update)
VALUES(9972, 10755, 1593469222, 1546374845);
REPLACE
INTO ifc_media(plex_media_id, plex_metadata_item_id,plex_media_last_update,plex_metadata_last_update)
VALUES(9695, 10637, 1593469111, 1537104922);

--below two will be with wrong plex_metadata_last_update
--correct plex_metadata_last_update for 9888 = 1546256610, and for 9973 = 1546639968
REPLACE
INTO ifc_media(plex_media_id, plex_metadata_item_id,plex_media_last_update,plex_metadata_last_update)
VALUES(9888, 10725, 1593469660, 1546256555);
REPLACE
INTO ifc_media(plex_media_id, plex_metadata_item_id,plex_media_last_update,plex_metadata_last_update)
VALUES(9973, 10756, 1593469499, 1546639333);

--below two will be with wrong both and plex_media_last_update and plex_metadata_last_update 
--correct plex_media_last_update for 10135 = 1593469469, and for 10136 = 1593469516
--correct plex_metadata_last_update for 10135 = 1556921126, and for 10135 = 1556921835
REPLACE
INTO ifc_media(plex_media_id, plex_metadata_item_id,plex_media_last_update,plex_metadata_last_update)
VALUES(10135, 10824, 1593469444, 1546256555);
REPLACE
INTO ifc_media(plex_media_id, plex_metadata_item_id,plex_media_last_update,plex_metadata_last_update)
VALUES(10136, 10825, 1593469666, 1546639777);


-- below are missing in plex
REPLACE
INTO ifc_media(plex_media_id, plex_metadata_item_id,plex_media_last_update,plex_metadata_last_update)
VALUES(2222, 113411, 1536430189, 1536430189);
REPLACE
INTO ifc_media(plex_media_id, plex_metadata_item_id,plex_media_last_update,plex_metadata_last_update)
VALUES(3333, 113411, 1536430189, 1536430189);

--DELETE FROM ifc_media
--WHERE plex_media_id = ;



INSERT INTO ifc_media (
    plex_media_id,
    plex_metadata_item_id,
    name,
    is_series,
    stalker_category_id,
    stalker_genere_id,
    plex_media_last_update,
    plex_metadata_last_update)
VALUES (
    9415,
    10533,
    'Beauty and the Beast',
    0,
    1,
    6,
    CAST(strftime('%s', '2018-03-31 01:02:03') AS INTEGER),
    CAST(strftime('%s', '2018-03-31 01:02:03') AS INTEGER));
