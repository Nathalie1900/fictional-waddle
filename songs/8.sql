-- In 8.sql, write a SQL query that lists the names of the songs that feature other artists.
-- Songs that feature other artists will include “feat.” in the name of the song.
-- Your query should output a table with a single column for the name of each song.

-- Exercise proposed by my mom:
-- SELECT COUNT(*) FROM songs WHERE artist_id=
-- (SELECT id FROM artists WHERE name = 'Daddy Yankee');

SELECT name FROM songs WHERE name LIKE '%feat.%';
