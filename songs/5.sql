-- In 5.sql, write a SQL query that returns the average energy of all the songs.
-- Your query should output a table with a single column and a single row containing the average energy.
SELECT AVG(energy) AS average_energy FROM songs;
-- SELECT AVG(valence) AS average_valence FROM songs;
-- SELECT AVG(danceability) AS average_danceability FROM songs;
