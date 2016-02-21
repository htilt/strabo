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

CREATE TABLE IF NOT EXISTS text_selections (
	id INTEGER PRIMARY KEY,
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
	name TEXT,
	book TEXT,
	section TEXT,
	pages TEXT,
	passage TEXT,
	interest_point TEXT,
	event TEXT,
	notes TEXT,
	tags TEXT,
	edited_by TEXT);
