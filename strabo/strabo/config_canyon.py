from strabo import app

#
#
#
#
###### The following variables require configuration.

# set the latitude and longitude for the center of the map
# these values will be passed into the js file that gets rewritten
# each time interest points are updated by the administrator, so
# changes here will not be reflected until an interest point is
# added, edited, or deleted.
app.config['LAT_SETTING'] = 45.481851
app.config['LONG_SETTING'] = -122.630397
# set periods for uploading images and searching timeline
#### CHANGE TO: one for each decade? ####
app.config['PERIODS'] = ('1900 to 1920s', '1930s', '1940s', '1950s','1960s','1970s','1980s','1990s','2000s','2010s')
# set feature types for uploading interest points
app.config['FEATURE_TYPES'] = ("Historical Feature", "Plant",
  "Tree", "Building", "Trail", "Pipe", "Bridge",
  "Natural Feature", "Recreational Facility","Water Feature","Other")

#
#
#
#
##### set preferred styles, website title, and headings
##### "About" page ("about.html") must be edited directly.

# Choose between reedred_base.css, berkeleyblue_base.css, and minwhite_base.css
app.config['BASE_CSS'] = "reedred_base.css"

# set website title
app.config['WEBSITE_TITLE'] = 'Discover the Reed College Canyon'
# set greeting on homepage for admin end
app.config['INDEX_GREETING'] = "Select a tab to begin adding content to the Canyon."
# set title and subtitle for image gallery
app.config['GALLERY_TITLE'] = "Image Gallery"
app.config['GALLERY_SUBTITLE'] = "Reed College Canyon Past and Present"
# timeline functionality is currently disabled
# set title and subtitle for timeline
app.config['TIMELINE_TITLE'] = "Timeline of Major Events"
app.config['TIMELINE_SUBTITLE'] = "Scroll to explore the major events in the history of the canyon."

#
#
#
#
###### The following variables probably will not require configuration.

#
app.config['IS_DEBUG'] = True
# set absolute and relative paths to the upload directory for images
app.config['UPLOAD_FOLDER'] = '../strabo/strabo/static/uploads-livy/'
app.config['UPLOAD_FOLDER_RELPATH'] = '/static/uploads-livy/'
# set absolute and relative paths to the upload directory for thumbnails
app.config['NEW_DATA_DIRECTORY'] = '../strabo/strabo/static/thumbnails-livy/'
app.config['NEW_DATA_DIRECTORY_RELPATH'] = '/static/thumbnails-livy/'
# set folder name for javascript
app.config['JS_FOLDER'] = '../strabo/strabo/static/js/'
# set filename for file containing interest point geojson objects
app.config['INTPT_FILE'] = 'interest_points_livy.js'
# set filename for js file with Leaflet for public map
app.config['MAP_JS'] = 'map-livy.js'
# set filename for js file with Leaflet for private, admin end map
# with draw functionality
app.config['DRAWMAP_JS'] = 'drawMap-livy.js'
# set absolute and relative paths to styles
app.config['PATH_TO_PUBLIC_STYLES'] = "../static/public_styles/"
app.config['RELPATH_TO_PUBLIC_TEMPLATES'] = "public/"

# set template filenames
app.config['MAP_TEMPLATE'] = "map.html"
app.config['BASE_TEMPLATE'] = "base.html"
app.config['HEADER_TEMPLATE'] = "header.html"
app.config['FOOTER_TEMPLATE'] = "footer.html"

# set stylesheet filenames
app.config['HEADER_CSS'] = "header.css"
app.config['FOOTER_CSS'] = "footer.css"
app.config['MAP_CSS'] = "map.css"
app.config['GALLERY_CSS'] = "gallery.css"
app.config['TIMELINE_CSS'] = "timeline.css"
app.config['UNDER_CONST_CSS'] = 'under_const.css'
app.config['ABOUT_CSS'] = 'about.css'

# set allowed extensions for uploaded images
app.config['ALLOWED_EXTENSIONS'] = set(['pdf', 'png', 'jpg', 'jpeg', 'JPG', 'JPEG'])

# set the map tile source, attribution, subdomains, and extension.
# if you wish to use different map tiles that take other variables,
# you will need to edit map.js directly.
app.config["MAP_TILE_SRC"] = 'http://{s}.tile.thunderforest.com/pioneer/{z}/{x}/{y}.png'
app.config["MAP_ATTR1"] = '&copy; <a href="http://www.thunderforest.com/">Thunderforest</a>, &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
app.config["SUBDOMAINS"] = 'abcd'
app.config["EXTENSION"] = 'png'

# list the columns that users should be able to search in the public gallery
app.config['IMAGE_SEARCH_COLUMNS'] = ['title', 'img_description', 'latitude', 'longitude',
'interest_point', 'event', 'period', 'notes']

app.config['FUZZY_SEARCH_COLUMNS'] = ["title", "img_description", "event_description", "name",
    "passage", "tags", "notes"]

#flask_sqlalchemy specific configuations
# set name of database
#app.config['SQLALCHEMY_DATABASE_URI']  = "postgres://localhost/strabo_test"
app.config['SQLALCHEMY_DATABASE_URI']  = "sqlite:///../sqlalchemy_data.sqlite3"
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#
#
#
#
###### The following variables probably will not require configuration.

# Provide aliases for column names
# Only edit column aliases if coulumns in schema.py have been altered.
app.config['COLUMN_ALIASES'] = {'id':'Integer ID', 'created_at':'Time Added to Database', 'title':'Title',
  'img_description':'Image Description', 'latitude':'Latitude', 'longitude':'Longitude',
  'date_created':'Date Created', 'interest_point':'Interest Point', 'event':'Event',
  'period':'Period', 'notes':'Notes', 'tags':'Tags', 'edited_by':'Editor', 'filename':'Image Filename',
  'thumbnail_name':'Image Thumbnail Filename', 'event_description':'Event Description',
  'date_of_event':'Date of Event', 'name':'Name', 'books':'Books', 'coordinates':'Coordinates',
  'geojson_object':'Geojson Object', 'feature_type':'Feature Type', 'book':'Book',
  'geojson_feature_type': 'Geojson Feature Type', 'section':'Section', 'pages':'Pages',
  'passage':'Passage'}

# make a reverse dictionary of aliases
def reverse_aliases(column_aliases):
  column_aliases_tuples = column_aliases.items()
  rev_dict = {}
  for tup in column_aliases_tuples:
    x, y = tup
    rev_dict[y] = x
  return rev_dict

app.config['REVERSE_COLUMN_ALIASES'] = reverse_aliases(app.config['COLUMN_ALIASES'])
