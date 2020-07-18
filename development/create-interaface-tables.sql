---------------Keep the statements here for future use ------------------
-- CREATE TABLE ifc_media (
--     plex_media_id INTEGER,
--     plex_metadata_item_id INTEGER NOT NULL,
--     plex_media_last_update INTEGER,
--     plex_metadata_last_update INTEGER NOT NULL,
--     stalker_video_id INTEGER,
--     ifc_update_stalker INTEGER DEFAULT 0,
--     ifc_for_deletion INTEGER DEFAULT 0,
--     is_series INTEGER DEFAULT 0,
--     updt_video INTEGER DEFAULT 0,
--     updt_files INTEGER DEFAULT 0,
--     updt_seas INTEGER DEFAULT 0,
--     updt_series INTEGER DEFAULT 0,
--     UNIQUE(plex_metadata_item_id, stalker_video_id)
-- );

-- CREATE UNIQUE INDEX idx_plex_metadata_item_id
-- ON ifc_media(plex_metadata_item_id);

-- DROP INDEX idx_season_metadata_id;

-- SELECT * from sqlite_master where TYPE = 'trigger';
-- SELECT * from sqlite_master where TYPE = 'index';
-- DROP TRIGGER set_stalker_update_on_insert;
-- DROP TRIGGER set_stalker_update_on_update;
-- DROP TRIGGER set_seas_update_on_insert;

-- CREATE TRIGGER set_stalker_update_on_insert AFTER INSERT
-- ON ifc_media
-- FOR EACH ROW
-- BEGIN
--     UPDATE ifc_media
--         SET updt_video = 1,
--             updt_files = 1,
--             updt_seas = 1,
--             updt_series = 1
--     WHERE plex_metadata_item_id = NEW.plex_metadata_item_id;
-- END;

-- CREATE TRIGGER set_stalker_update_on_update
-- AFTER UPDATE
-- ON ifc_media
-- WHEN (NEW.stalker_video_id IS NULL)
-- BEGIN
--     UPDATE ifc_media
--         SET updt_video = 1,
--             updt_files = 1,
--             updt_seas = 1,
--             updt_series = 1        
--     WHERE plex_metadata_item_id = NEW.plex_metadata_item_id;
-- END;


-- CREATE TABLE "ifc_tv_seasons" (
--     "series_metadata_id" INTEGER,
--     "season_metadata_id" INTEGER NOT NULL,
--     "season_index" INTEGER,
--     "nbr_episodes" INTEGER,
--     "metadata_last_update" INTEGER,
--     "stalker_video_id" INTEGER,
--     "stalker_season_id" INTEGER,
--     "ifc_update_stalker" INTEGER DEFAULT 0,
--     "updt_seas" INTEGER DEFAULT 0,
--     "updt_episodes" INTEGER DEFAULT 0,
--     "for_deletion" INTEGER DEFAULT 0,
--     UNIQUE("season_metadata_id", "stalker_season_id")
-- );

-- CREATE UNIQUE INDEX "idx_season_metadata_id"
-- ON "ifc_tv_seasons"("season_metadata_id");

-- DROP INDEX idx_season_metadata_id;



-- CREATE TABLE "ifc_episodes" (
--     "season_metadata_id" INTEGER NOT NULL,
--     "media_item_id" INTEGER NOT NULL,
--     "number_of_files" INTEGER,
--     "stalker_video_id" INTEGER,
--     "stalker_season_id" INTEGER,
--     "stalker_video_series_file_id" INTEGER,
--     "ifc_update_stalker" INTEGER DEFAULT 0,
--     "updt_episodes" INTEGER DEFAULT 0,
--     "for_deletion" INTEGER DEFAULT 0,
--     UNIQUE("media_item_id", "stalker_video_series_file_id")
-- );

-- CREATE UNIQUE INDEX "idx_episode_media_item_id"
-- ON "ifc_episodes"("media_item_id");

-- DROP INDEX idx_episode_media_item_id;

--------------End of Keep---------------------------------------------------



--DROP TABLE ifc_episodes;

--UPDATE ifc_media SET ifc_update_stalker = 0;

--SELECT * from ifc_media WHERE ROW = 1;

-- ALTER TABLE ifc_media
-- RENAME COLUMN updt_video_1
-- TO updt_video;

-- ALTER TABLE ifc_media
-- RENAME TO ifc_media_b;

-- ALTER TABLE ifc_episodes
-- RENAME TO ifc_episodes_b;

-- INSERT INTO ifc_media SELECT * FROM ifc_media_b;

-- SELECT * from ifc_media;
-- SELECT * from ifc_media_b;

-- ALTER TABLE ifc_episodes
-- ADD COLUMN stalker_season_id INTEGER;

-- DELETE from ifc_tv_seasons;