SELECT 
    library_sections.name AS Libary, 
    metadata_series.title as Series, 
    metadata_season.'index' AS Season, 
    metadata_media.title AS Title 
FROM media_items
INNER JOIN metadata_items as metadata_media
ON media_items.metadata_item_id = metadata_media.id
LEFT JOIN metadata_items as metadata_season
ON metadata_media.parent_id = metadata_season.id
LEFT JOIN metadata_items as metadata_series
ON metadata_season.parent_id = metadata_series.id
INNER JOIN section_locations
ON media_items.section_location_id = section_locations.id
INNER JOIN library_sections
ON library_sections.id = section_locations.library_section_id
WHERE media_items.section_location_id IN(8,10);


SELECT 
    library_sections.name AS Libary, 
    metadata_series.title as Series, 
    metadata_season.'index' AS Season, 
    metadata_media.title AS Title 
FROM media_items
INNER JOIN metadata_items as metadata_media
ON media_items.metadata_item_id = metadata_media.id
LEFT JOIN metadata_items as metadata_season
ON metadata_media.parent_id = metadata_season.id
LEFT JOIN metadata_items as metadata_series
ON metadata_season.parent_id = metadata_series.id
INNER JOIN section_locations
ON media_items.section_location_id = section_locations.id
INNER JOIN library_sections
ON library_sections.id = section_locations.library_section_id

