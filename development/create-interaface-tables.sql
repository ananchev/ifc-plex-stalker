CREATE TABLE ifc_media (
    plex_media_id INTEGER NOT NULL,
    plex_metadata_item_id INTEGER NOT NULL,
    plex_media_last_update INTEGER NOT NULL,
    plex_metadata_last_update INTEGER NOT NULL,
    stalker_video_id INTEGER,
    ifc_update_stalker INTEGER DEFAULT 0,
    ifc_for_deletion INTEGER DEFAULT 0,
    UNIQUE(plex_media_id, plex_metadata_item_id, stalker_video_id)
);

CREATE UNIQUE INDEX idx_plex_media_id
ON ifc_media(plex_media_id);

DROP INDEX idx_plex_media_id;

DROP TABLE ifc_media_b;

UPDATE ifc_media SET ifc_update_stalker = 0;


ALTER TABLE ifc_media
RENAME COLUMN ifc_last_update
TO plex_media_last_update;

ALTER TABLE ifc_media
RENAME TO ifc_media_b;

INSERT INTO ifc_media SELECT * FROM ifc_media_b;

SELECT * from ifc_media;

ALTER TABLE ifc_media
ADD COLUMN plex_metadata_last_update INTEGER;
