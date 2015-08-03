CREATE TABLE IF NOT EXISTS images (
	id INTEGER PRIMARY KEY,
	title TEXT,
	img_description TEXT,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	latitude REAL,
	longitude REAL,
	period TEXT,
	interest_point TEXT,
	notes TEXT,
	filename TEXT,
	thumbnail_name TEXT);

CREATE TABLE IF NOT EXISTS events (
	id INTEGER PRIMARY KEY,
	title TEXT,
	event_description TEXT,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	year REAL,
	notes TEXT);

CREATE TABLE IF NOT EXISTS interest_points (
	id INTEGER PRIMARY KEY,
	name TEXT,
	latitude REAL,
	longitude REAL,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	notes TEXT);

-- ALTER TABLE images ADD COLUMN events

-- sqlite> ALTER TABLE images ADD COLUMN fav_food
--    ...> ;
-- sqlite> SELECT * from images;
-- 1|Shirley|2015-07-31 01:10:29|
-- 2|Tom|2015-07-31 01:10:51|
-- 3|Samantha|2015-07-31 01:11:06|
-- 4|Chris|2015-07-31 01:11:17|
-- sqlite> UPDATE images
--    ...> SET fav_food = 'chocolate'
--    ...> WHERE ID = 1;
-- sqlite> SELECT * from images;
-- 1|Shirley|2015-07-31 01:10:29|chocolate
-- 2|Tom|2015-07-31 01:10:51|
-- 3|Samantha|2015-07-31 01:11:06|
-- 4|Chris|2015-07-31 01:11:17|
-- sqlite> UPDATE images
--    ...> SET fav_food = 'lettuce'
--    ...> WHERE name = 'Tom';
-- sqlite> SELECT * from images;
-- 1|Shirley|2015-07-31 01:10:29|chocolate
-- 2|Tom|2015-07-31 01:10:51|lettuce
-- 3|Samantha|2015-07-31 01:11:06|
-- 4|Chris|2015-07-31 01:11:17|
-- sqlite> 
