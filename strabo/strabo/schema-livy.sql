CREATE TABLE IF NOT EXISTS images (
	id INTEGER PRIMARY KEY,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	title TEXT,
	img_description TEXT,
	latitude REAL,
	longitude REAL,
	date_created TEXT,
	interest_point TEXT,
	event TEXT,
	period TEXT,
	notes TEXT,
	tags TEXT,
	edited_by TEXT,
	filename TEXT,
	thumbnail_name TEXT);

CREATE TABLE IF NOT EXISTS events (
	id INTEGER PRIMARY KEY,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	title TEXT,
	event_description TEXT,
	date_of_event TEXT,
	notes TEXT,
	tags TEXT,
	edited_by TEXT);

CREATE TABLE IF NOT EXISTS interest_points (
	id INTEGER PRIMARY KEY,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	name TEXT,
	books TEXT,
	coordinates TEXT,
	geojson_object TEXT,
	feature_type TEXT,
	geojson_feature_type TEXT,
	notes TEXT,
	tags TEXT,
	edited_by TEXT);

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
