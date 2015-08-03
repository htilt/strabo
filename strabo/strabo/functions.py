import sqlite3, os, os.path
from contextlib import closing

from PIL import Image

from strabo import app

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This function starts a new connection to the bbs.sqlite3 database.
def get_db():
  conn = sqlite3.connect("bbs.sqlite3")
  return conn

# This function loads in the proper sql table if it doesn't already exist.
def migrate_db():
  with closing(get_db()) as db:
    with app.open_resource('schema.sql', mode='r') as fh:
      db.cursor().executescript(fh.read())
      db.commit()

# This helper function uses PIL to make a new thumbnail of a given image
def make_thumbnail(filename):
  # import desired image from /uploads folder
  img = Image.open(app.config['UPLOAD_FOLDER'] + '/' + filename)
  # create a thumbnail from desired image
  size = 300, 300
  img.thumbnail(size)
  # save the image under a new filename in thumbnails directory
  imagename = filename.split(".")
  # functional version: imagename = filename.rsplit(".", 1)[0]
  newfilename = imagename[0] + "_thumbnail.jpeg"
  path = app.config['NEW_DATA_DIRECTORY']
  fullpath = os.path.join(path, newfilename)
  img.save(fullpath)
  # return the filename for the thumbnail
  return newfilename

def image_handler(year=None, event=None, location=None):
  if year is not None:
    return handler_helper('year', year)
  if event is not None:
    return handler_helper('event', event)
  else:
    return handler_helper('interest_point', location)

def handler_helper(field, variable):
  with closing(get_db()) as db:
        # Query db for the first five images for the selected interest_point.
        images = db.execute(
          "SELECT filename, title FROM images WHERE %s = '%s' ORDER by id DESC LIMIT 12" % (field, variable)
        ).fetchall()
    # Passes values from each image to template as tuple (containing only one element), stored in list-array 'images'
  return images

def get_images(ip_value):
  with closing(get_db()) as db:
        # Query db for the first five images for the selected interest_point.
        images = db.execute(
          "SELECT thumbnail_name, interest_point FROM images WHERE interest_point = '%s' ORDER by id DESC LIMIT 5" % ip_value
        ).fetchall()
    # Passes values from each image to template as tuple (containing only one element), stored in list-array 'images'
  return images

def get_12_images(ip_value=None):
  if ip_value:
    with closing(get_db()) as db:
      # Query db for the images.
      images = db.execute("SELECT filename, title, created_at FROM images WHERE interest_point = '%s' ORDER by id DESC LIMIT 12" % ip_value
        ).fetchall()
  else:
    with closing(get_db()) as db:
      # Query db for the images.
      images = db.execute("SELECT filename, title, created_at FROM images ORDER by id LIMIT 12").fetchall()
  # Passes values from each image to template as tuple (containing only one element), stored in list-array 'images'
  return images

def get_events():
  with closing(get_db()) as db:
    events = db.execute("SELECT title, event_description, year, notes FROM events ORDER by id").fetchall()
    print(events)
  return events

def get_interest_points():
  with closing(get_db()) as db:
    interest_points = db.execute("SELECT name, latitude, longitude, notes FROM interest_points ORDER by id DESC"
      ).fetchall()
  return interest_points

def get_images_flex():
  with closing(get_db()) as db:
    images = db.execute(
        "SELECT title, img_description, created_at, latitude, longitude, period, interest_point, notes, filename, thumbnail_name FROM images ORDER by id DESC LIMIT 10"
      ).fetchall()
    return images

def get_column_names(table_name):
  with closing(get_db()) as db:
    c = db.cursor()
    c.execute('SELECT * FROM images')
    column_names = c.description
    # column_names = db.execute("SELECT sql FROM sqlite_master WHERE tbl_name = 'images' AND type = 'table'")
  return column_names
  
def search_images(column, search_term):
  with closing(get_db()) as db:
    images = db.execute("SELECT * FROM images WHERE %s = '%s' ORDER by id DESC" % (column, search_term)
      ).fetchall()
  return images

def delete(keys):
  with closing(get_db()) as db:
    c = db.cursor()
    # keys = [map(int, x) for x in keys]
    print(keys)
    # for key in keys:
    #   print(type(key))
    #   integer = int(key)
    #   print(type(integer))
    #   c.execute('DELETE FROM images WHERE id =' + key)
  return
