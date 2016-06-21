import enum
# make a reverse dictionary of aliases
def reverse_dict(forward_dict):
  return {v:k for k,v in forward_dict.items()}

# set feature types for uploading interest points
class Layers(enum.Enum):
    plant = 1
    animal = 2
    hist = 3
    cool = 4

def config_app(app):
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
    app.config['INITIAL_ZOOM'] = 17

    app.config['LAYER_FIELDS'] = lay_fields = {
            Layers.plant:"Plants",
            Layers.animal:"Animals",
            Layers.hist:"Interest Points",
            Layers.cool:"Sensitive Areas"
        }

    app.config['LAYER_FIELD_ENUMS'] = reverse_dict(lay_fields)


    #
    ##### set preferred styles, website title, and headings
    ##### "About" page ("about.html") must be edited directly.

    app.config['BASE_CSS'] = "canyon_base.css"
    app.config['HEADER_CSS'] = "header.css"
    app.config['FOOTER_CSS'] = "footer.css"
    app.config['MAP_CSS'] = "map.css"
    app.config['GALLERY_CSS'] = "gallery.css"
    app.config['ABOUT_CSS'] = 'about.css'

    app.config['WEBSITE_TITLE'] = 'Discover the Reed College Canyon'
    app.config['INDEX_GREETING'] = "Select a tab to begin adding content to the Canyon."

    # set title and subtitle for image gallery
    app.config['GALLERY_TITLE'] = "Image Gallery"
    app.config['GALLERY_SUBTITLE'] = "Reed College Canyon Past and Present"

    app.config['MAP_TEMPLATE'] = "map.html"
    app.config['BASE_TEMPLATE'] = "base.html"
    app.config['HEADER_TEMPLATE'] = "header.html"
    app.config['FOOTER_TEMPLATE'] = "footer.html"

    app.config['MAP_JS'] = 'map.js'
    app.config['ADMINMAP_JS'] = 'drawMap.js'
    app.config['FAVICON'] = '../strabo/strabo/static/favicon.ico'


    ###### The following variables probably will not require configuration.
    # set absolute and relative paths to the upload directory for images
    app.config['UPLOAD_FOLDER'] = '../strabo/strabo/static/uploads/'
    app.config['UPLOAD_FOLDER_RELPATH'] = '/static/uploads/'
    # set absolute and relative paths to the upload directory for thumbnails
    app.config['NEW_DATA_DIRECTORY'] = '../strabo/strabo/static/thumbnails/'
    app.config['NEW_DATA_DIRECTORY_RELPATH'] = '/static/thumbnails/'
    # set folder name for javascript
    app.config['JS_FOLDER'] = '../strabo/strabo/static/js/'


    # set absolute and relative paths to styles
    app.config['PATH_TO_PUBLIC_STYLES'] = "../static/public_styles/"
    app.config['RELPATH_TO_PUBLIC_TEMPLATES'] = "public/"

    app.config['ALLOWED_EXTENSIONS'] = {'png','PNG','jpg', 'jpeg', 'JPG', 'JPEG'}

    app.config["MAP_TILE_SRC"] = 'http://{s}.tile.thunderforest.com/outdoors/{z}/{x}/{y}.png'
    app.config['LEAFLET_ATTRIBUTES'] = {
        "attribution":'Map tiles by Thunderforest, Map data by OpenStreetMap',
        "minZoom": 14,
        "maxZoom": 22,
        "ext": 'png'
    }

    app.config['SQLALCHEMY_DATABASE_URI']  = "postgres://localhost/strabo"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  = False
    app.config['DEBUG']  = True

    app.config["THUMBNAIL_MAX_SIZE"] = (300,250)#max_width, max_height

    ###### The following variables probably will not require configuration.

    # Provide aliases for column names
    # Only edit column aliases if coulumns in schema.py have been altered.
    app.config['COLUMN_ALIASES'] = {'id':'Integer ID', 'name':'Name',
      'layer':'Layer Name',
      'interest_point_id':'Interest Point',
      'filename':'Filename',
      'thumbnail_name':'Image Thumbnail Filename',
      'geojson_object':'Geojson Object',
      'geojson_feature_type': 'Geojson Feature Type'
      }


    app.config['REVERSE_COLUMN_ALIASES'] = reverse_dict(app.config['COLUMN_ALIASES'])
