from strabo import app
# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = '../strabo/strabo/static/uploads-livy'
app.config['UPLOAD_FOLDER_RELPATH'] = '/static/uploads-livy/'

# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['pdf', 'png', 'jpg', 'jpeg', 'JPG', 'JPEG'])
# Set paths, to be called later
app.config['NEW_DATA_DIRECTORY'] = '../strabo/strabo/static/thumbnails-livy/'
app.config['NEW_DATA_DIRECTORY_RELPATH'] = '/static/thumbnails-livy/'

# set the db
app.config['DATABASE'] = "livy.sqlite3"
# set the db schema
app.config["SCHEMA"] = "schema-livy.sql"
# set periods for searching
app.config['PERIODS'] = ['Republican', 'Augustan', 'Imperial', 'Modern']
app.config['PERIOD_TYPE'] = 'eras'
app.config['ALL_PERIODS'] = "All Eras"
app.config['PERIOD_COLUMN'] = "period"

app.config['INSERT_IMG_QUERY'] = """INSERT INTO images(title, img_description, 
latitude, longitude, date_created, interest_point, event, period, notes, 
tags, edited_by, filename, thumbnail_name) VALUES(?, ?, ?, ?, ?, ?,
?, ?, ?, ?, ?, ?, ?)"""
app.config['EDIT_IMG_QUERY'] = """REPLACE INTO images 
VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

app.config['INSERT_IP_QUERY'] = """INSERT INTO interest_points(name, books,
coordinates, geojson_object, feature_type, geojson_feature_type, notes, tags, 
edited_by) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"""
app.config['EDIT_IP_QUERY'] = """REPLACE INTO interest_points VALUES(?, ?, ?, ?, ?, 
?, ?, ?, ?, ?, ?)"""

app.config['INSERT_EVENT_QUERY'] = """INSERT INTO events
(title, event_description, date_of_event, notes, tags, edited_by) 
VALUES(?, ?, ?, ?, ?, ?)"""
app.config['EDIT_EVENT_QUERY'] = """REPLACE INTO events VALUES(?, ?, ?, ?, ?, ?,
?, ?)"""

app.config['INSERT_TEXT_QUERY'] = """INSERT INTO text_selections
(name, book, section, pages, passage, interest_point, event,
notes, tags, edited_by) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

app.config['JS_FOLDER'] = '../strabo/strabo/static/js/'
app.config['INTPT_FILE'] = 'interest_points_livy.js'
app.config['MAP_JS'] = 'map-livy.js'
app.config['DRAWMAP_JS'] = 'drawMap-livy.js'

app.config['MAP_TEMPLATE'] = "map.html"
app.config['BASE_TEMPLATE'] = "base.html"
app.config['HEADER_TEMPLATE'] = 'header-livy.html'
app.config['HEADER_CSS'] = 'header.css'
app.config['PATH_TO_PUBLIC_STYLES'] = "../static/public_styles/"
app.config['RELPATH_TO_PUBLIC_TEMPLATES'] = "public/"
app.config['FOOTER_TEMPLATE'] = "footer.html"
app.config['FOOTER_CSS'] = "footer.css"

app.config['GALLERY_TITLE'] = "Image Gallery"
app.config['GALLERY_SUBTITLE'] = "Livy's Rome Past and Present"

app.config['TIMELINE_TITLE'] = "Timeline of Major Events"
app.config['TIMELINE_SUBTITLE'] = "Scroll to explore the major events in the first five books of Ab Urbe Condita."

app.config['WEBSITE_TITLE'] = 'Reconstructing Livy\'s Rome'


#### Changes made to config since last divergence from master branch
app.config['INDEX_GREETING'] = "Select a tab to begin adding content to Livy's Rome."