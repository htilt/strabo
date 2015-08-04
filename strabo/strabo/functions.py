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
  imagename = filename.rsplit(".", 1)[0]
  newfilename = imagename + "_thumbnail.jpeg"
  path = app.config['NEW_DATA_DIRECTORY']
  fullpath = os.path.join(path, newfilename)
  img.save(fullpath)
  # return the filename for the thumbnail
  return newfilename

# This function ensures that handler_helper will receive a safe 
# column name.
def image_handler(year=None, event=None, location=None):
  if year is not None:
    return handler_helper('year', year)
  if event is not None:
    return handler_helper('event', event)
  else:
    return handler_helper('interest_point', location)

# Gets 12 images from db for which a given column mathes the user input.
def handler_helper(column, variable):
  with closing(get_db()) as db:
    query = """SELECT filename, title FROM images WHERE {column} = ? 
      ORDER by id LIMIT 12""".format(column = column)
    images = db.execute(query, (variable,)).fetchall()
    # Passes values from each image to template as tuple 
    # (containing only one element), stored in list-array 'images'
  return images

# Gets 5 images from db for which the interest_point column matches the user input.
def get_images(ip_value):
  with closing(get_db()) as db:
    query = """SELECT thumbnail_name, interest_point FROM images 
      WHERE interest_point = ? ORDER by id DESC LIMIT 5"""
    images = db.execute(query, (ip_value,)).fetchall()
    # Passes values from each image to template as tuple 
    # (containing only one element), stored in list-array 'images'
  return images

# Gets 12 images whether or not an interest point is supplied as a variable.
def get_12_images(ip_value=None):
  if ip_value:
    with closing(get_db()) as db:
      query = """SELECT filename, title, created_at FROM images 
        WHERE interest_point = ? ORDER by id DESC LIMIT 12"""
      images = db.execute(query, (ip_value,)).fetchall()
  else:
    with closing(get_db()) as db:
      query = """SELECT filename, title, created_at 
        FROM images ORDER by id LIMIT 12"""
      images = db.execute(query).fetchall()
  # Passes values from each image to template as tuple 
  # (containing only one element), stored in list-array 'images'
  return images

# Gets all events from events table
def get_events():
  with closing(get_db()) as db:
    events = db.execute("""SELECT title, event_description, 
      year, notes FROM events ORDER by id""").fetchall()
  return events

# Gets all interest points from interest_points table
def get_interest_points():
  with closing(get_db()) as db:
    interest_points = db.execute("""SELECT name, latitude, longitude, 
      notes FROM interest_points ORDER by id DESC"""
      ).fetchall()
  return interest_points

# Gets 10 images with select metadata
def get_images_flex():
  with closing(get_db()) as db:
    images = db.execute(
        """SELECT title, img_description, created_at, latitude, longitude, period, 
        interest_point, notes, filename, thumbnail_name FROM images 
        ORDER by id DESC LIMIT 10""").fetchall()
    return images

# Gets column names from a given table
def get_column_names(table_name):
  with closing(get_db()) as db:
    c = db.cursor()
    c.execute('SELECT * FROM {table}'.format(table=table_name))
    column_names = c.description
  return column_names

SCHEMA = {
  'images': [c[0] for c in get_column_names('images')],
  'events': [c[0] for c in get_column_names('events')],
  'interest_points': [c[0] for c in get_column_names('interest_points')]
}

### Although table name is secure (sent to the function by the server, and not prone to SQL
### injection), column name is not secure, and could be subject to SQL injection via 
### a $.POST() request.
def search(table_name, column, search_term):
  if not table_name in SCHEMA:
    return []
  if not column in SCHEMA[table_name]:
    return []

  with closing(get_db()) as db:
    if column in ("title", "img_description", "event_description", "name"):
      query = """SELECT * FROM {table} WHERE {column} LIKE ?
        ORDER BY id DESC""".format(table=table_name, column=column)
      search_term = '%{}%'.format(search_term)
    else:
      query = """SELECT * FROM {table} WHERE {column} = ?
        ORDER by id DESC""".format(table=table_name, column=column)
    data = db.execute(query, (search_term,)).fetchall()
  return data

# SEARCH_VAR_PATTERN = re.compile(r'^[\w_]+$')

def get_all(table_name):
  with closing(get_db()) as db:
    data = db.execute("SELECT * FROM {table} ORDER by id".format(table=table_name)).fetchall()
  return data

def delete(keys, table_name):
  with closing(get_db()) as db:
    c = db.cursor()
    for key in keys:
      # if images is the table to be modified, delete the image from /uploads
      if table_name == "images":
        query = """SELECT filename FROM images WHERE id = ?"""
        file_name = c.execute(query, (key,)).fetchall()
        file_name = (file_name[0][0])
        path = app.config['UPLOAD_FOLDER']
        fullpath = os.path.join(path, file_name)
        os.remove(fullpath)
      # then delete the db row
      query = """DELETE FROM {table} WHERE id = ?""".format(table=table_name)
      db.execute(query, (key,))
    db.commit()
  return

def insert_images(params):
  # Create a tuple 'params' containing all of the variables from above.
  # Pass it to the cursor and commit changes.
  with closing(get_db()) as db:
    db.cursor().execute("""INSERT INTO images(title, img_description, 
      latitude, longitude, period, interest_point, notes, filename, 
      thumbnail_name) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)""", params)
    db.commit()

def insert_ips(params):
  with closing(get_db()) as db:
    db.cursor().execute("""INSERT INTO interest_points
      (name, latitude, longitude, notes) VALUES(?, ?, ?, ?)""", params)
    db.commit()

def insert_events(params):
  with closing(get_db()) as db:
    db.cursor().execute("""INSERT INTO events
      (title, event_description, year, notes) VALUES(?, ?, ?, ?)""", params)
    db.commit()