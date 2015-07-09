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