INSERT INTO cat_genre (title, category_alias)
    SELECT * FROM (SELECT {0}, {1}) AS tmp
    WHERE NOT EXISTS (
        SELECT title FROM cat_genre WHERE title = {0}
    ) LIMIT 1