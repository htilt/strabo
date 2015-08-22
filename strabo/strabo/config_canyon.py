from strabo import app
from strabo.utils import list_years
# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = '../strabo/strabo/static/uploads'
app.config['UPLOAD_FOLDER_RELPATH'] = '/static/uploads/'

# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['pdf', 'png', 'jpg', 'jpeg', 'JPG', 'JPEG'])
# Set paths, to be called later
app.config['NEW_DATA_DIRECTORY'] = '../strabo/strabo/static/test_thumbnails/'
app.config['NEW_DATA_DIRECTORY_RELPATH'] = '/static/test_thumbnails/'
# set the db
app.config['DATABASE'] = "bbs.sqlite3"
DATABASE = "bbs.sqlite3"
# set the db schema
app.config["SCHEMA"] = "schema.sql"
# set periods for searching
app.config['PERIODS'] = list_years()
app.config['PERIOD_TYPE'] = 'years'
app.config['ALL_PERIODS'] = "All Years"
app.config['PERIOD_COLUMN'] = "date_created"

app.config['INSERT_IMG_QUERY'] = """INSERT INTO images(title, img_description, 
latitude, longitude, date_created, interest_point, event, notes, 
tags, edited_by, filename, thumbnail_name) VALUES(?, ?, ?, ?, ?,
?, ?, ?, ?, ?, ?, ?)"""
app.config['EDIT_IMG_QUERY'] = """REPLACE INTO images 
VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

app.config['INSERT_IP_QUERY'] = """INSERT INTO interest_points(name, coordinates, 
geojson_object, feature_type, geojson_feature_type, notes, tags, 
edited_by) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"""
app.config['EDIT_IP_QUERY'] = """REPLACE INTO interest_points VALUES(?, ?, ?, ?, ?, 
?, ?, ?, ?, ?)"""

app.config['INSERT_EVENT_QUERY'] = """INSERT INTO events
(title, event_description, date_of_event, notes, tags, edited_by) 
VALUES(?, ?, ?, ?, ?, ?)"""
app.config['EDIT_EVENT_QUERY'] = """REPLACE INTO events VALUES(?, ?, ?, ?, ?, ?,
?, ?)"""

app.config['JS_FOLDER'] = '../strabo/strabo/static/js/'
app.config['INTPT_FILE'] = 'interest_points.js'
app.config['MAP_JS'] = 'map.js'
app.config['DRAWMAP_JS'] = 'drawMap.js'

app.config['MAP_TEMPLATE'] = "map.html"
app.config['BASE_TEMPLATE'] = "base.html"
app.config['HEADER_TEMPLATE'] = 'header.html'
app.config['HEADER_CSS'] = 'header.css'
app.config['PATH_TO_PUBLIC_STYLES'] = "../static/public_styles/"
app.config['FOOTER_TEMPLATE'] = "footer.html"
app.config['FOOTER_CSS'] = "footer.css"

app.config['GALLERY_TITLE'] = "Canyon Image Gallery"
app.config['GALLERY_SUBTITLE'] = "from 1930 to now"

app.config['TIMELINE_TITLE'] = "Canyon Restoration Timeline"
app.config['TIMELINE_SUBTITLE'] = "Scroll to explore the history of the Reed Canyon and its restoration."

app.config['WEBSITE_TITLE'] = 'Canyon Mapping Project'
