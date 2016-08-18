import os
from strabo import utils

def get_config_info():
    config_info = dict()

    ###### The following variables require configuration.
    # set the latitude and longitude for the center of the map
    config_info['LAT_SETTING'] = 45.481851
    config_info['LONG_SETTING'] = -122.630397
    config_info['INITIAL_ZOOM'] = 17   #zoom if you are out of the canyon and in admin interface

    '''you can change the names of these, but do not change the numbers!
    If any items with the changed number are stored in the database strabo will break.'''
    config_info['LAYER_FIELDS'] = {
        1:"Plants",
        2:"Animals",
        3:"Interest Points",
        4:"Sensitive Areas"
    }
    config_info['REVERSE_LAYER_FIELDS'] = utils.reverse_dict(config_info['LAYER_FIELDS'])

    config_info['STRABO_ABS_PATH'] = strabo_abs_path = os.path.dirname(os.path.abspath(__file__))
    
# Color Icons for Interest Points
    config_info['COLOR_ICON'] = {
        "red": "Red.png",
        "orange": "Orange.png",
        "yellow": "Yellow.png",
        "green": "Green.png",
        "turquoise": "Turquoise.png",
        "navy": "Navy.png",
        "purple": "Purple.png",
        "magenta": "Magenta.png",
        "coral": "Coral.png",
        "evergreen": "Evergreen.png",
        "accesspooint": "AccessPoint.png",
        "sensitivearea": "SensitiveArea.png",
    }

# Color hex codes for Interest Zones
    config_info['COLOR_HEX'] = {
        "red": "#F40000",
        "orange": "#FF9955",
        "yellow": "#FFDD55",
        "green": "#00B100",
        "turquoise": "#00E3E3",
        "navy": "#002B66",
        "purple": "#EAB8F5",
        "magenta": "#CC0077",
        "coral": "#FF393D",
        "evergreen": "#006666",
        "accesspoint": "#606800",
        "sensitivearea": "#A7001E"
    }

# Color names for representation in drop down menu on admin end
    config_info['COLOR_REP'] = {
        "red": "Red",
        "orange": "Orange",
        "yellow": "Yellow",
        "green": "Green",
        "turquoise": "Turquoise",
        "navy": "Navy",
        "purple": "Purple",
        "magenta": "Magenta",
        "coral": "Coral",
        "evergreen": "Evergreen",
        "accesspoint": "Access Point",
        "sensitivearea": "Sensitive Area",
    }

# Colors stored in the database
    config_info['REVERSE_COLOR_REP'] = utils.reverse_dict(config_info['COLOR_REP'])

    ##### set preferred styles, website title, and headings
    ##### "About" page ("about.html") must be edited directly.

    config_info['BASE_CSS'] = "canyon_base.css"
    config_info['HEADER_CSS'] = "header.css"
    config_info['FOOTER_CSS'] = "footer.css"
    config_info['MAP_CSS'] = "map.css"
    config_info['GALLERY_CSS'] = "gallery.css"
    config_info['ABOUT_CSS'] = 'about.css'

    config_info['WEBSITE_TITLE'] = 'Discover the Reed College Canyon'
    config_info['INDEX_GREETING'] = "Select a tab to begin adding content to the Canyon."

    # set title and subtitle for image gallery
    config_info['GALLERY_TITLE'] = "Image Gallery"
    config_info['GALLERY_SUBTITLE'] = "Reed College Canyon Past and Present"

    config_info['MAP_TEMPLATE'] = "map.html"
    config_info['BASE_TEMPLATE'] = "base.html"
    config_info['HEADER_TEMPLATE'] = "header.html"
    config_info['FOOTER_TEMPLATE'] = "footer.html"

    config_info['MAP_JS'] = 'map.js'
    config_info['ADMINMAP_JS'] = 'drawMap.js'

 #####Login and Register stuff ##################
    config_info['LOGIN_HEADER'] = 'Strabo Login'
    config_info['LOGIN_GREETING'] = 'Login to continue adding content to the Canyon.'
    config_info['REGISTER_HEADER'] = 'Register for Strabo'
    config_info['REGISTER_GREETING'] = 'Register to begin adding content to the Canyon.'
    config_info['LOGIN_CSS'] = "login.css"


    ###### The following variables probably will not require configuration.
    # set absolute and relative paths to the upload directory for images
    config_info['UPLOAD_FOLDER'] = os.path.join(strabo_abs_path,'strabo/static/uploads/')
    config_info['UPLOAD_FOLDER_RELPATH'] = '/static/uploads/'
    # set absolute and relative paths to the upload directory for thumbnails
    config_info['MOBILE_IMG_DIR'] = os.path.join(strabo_abs_path,'strabo/static/mobile_imgs/')
    config_info['MOBILE_IM_DIR_RELPATH'] = '/static/mobile_imgs/'
    # set absolute and relative paths to the upload directory for
    config_info['THUMB_DIR'] = os.path.join(strabo_abs_path,'strabo/static/thumbnails/')
    config_info['THUMB_DIR_RELPATH'] = '/static/thumbnails/'


    # set absolute and relative paths to styles
    config_info['PATH_TO_PUBLIC_STYLES'] = "../static/public_styles/"
    config_info['RELPATH_TO_PUBLIC_TEMPLATES'] = "public/"

    config_info['ALLOWED_EXTENSIONS'] = ['png','PNG','jpg', 'jpeg', 'JPG', 'JPEG']

    config_info["MAP_TILE_SRC"] = 'https://{s}.tile.thunderforest.com/outdoors/{z}/{x}/{y}.png'
    config_info['LEAFLET_ATTRIBUTES'] = {
        "attribution":'Thunderforest tiles, OpenStreetMap data',
        "minZoom": 14,
        "maxZoom": 22,
        "ext": 'png'
    }

    #needs to correspond with popup view size
    config_info["THUMBNAIL_MAX_SIZE"] = (500,500)#max_width, max_height
    #larger images will make for slower animations and upload when navigating photoswipe
    config_info["MOBILE_SERV_MAX_SIZE"] = (1760,1500)#max_width, max_height

    return config_info


def config_app(app):
    '''
    Flask and sqlachemy specific configurations. These are kept seperate
    becuase unlike the others, they will change between development and deployment.
    '''
    app.config['SQLALCHEMY_DATABASE_URI']  = "postgres://localhost/strabo"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']  = False
    app.config['DEBUG']  = True
