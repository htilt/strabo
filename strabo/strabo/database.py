import sqlite3, os
from contextlib import closing

from strabo import app

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

def get_max_id():
  with closing(get_db()) as db:
    cur = db.cursor()
    cur = cur.execute('SELECT max(id) FROM images')
    max_id = cur.fetchone()[0]
  return max_id

# This function ensures that handler_helper will receive a safe 
# column name.
def get_images(year=None, event=None, location=None):
  if year is not None:
    return get_images_helper('year', year, 12)
  if event is not None:
    return get_images_helper('event', event, 12)
  else:
    return get_images_helper('interest_point', location, 12)

# Gets 12 images from db for which a given column matches the user input.
def get_images_helper(column, variable, count):
  with closing(get_db()) as db:
    db.row_factory = dict_factory
    cur = db.cursor()
    query = """SELECT * FROM images WHERE {column} = ? 
      ORDER by id LIMIT ?""".format(column = column)
    images = cur.execute(query, (variable, count)).fetchall()
  return images

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Gets 10 images with select metadata
def get_flex(table_name, count=None):
  with closing(get_db()) as db:
    db.row_factory = dict_factory
    cur = db.cursor()
    if count:
      query = """SELECT * FROM {table} ORDER BY id DESC LIMIT ?""".format(table=table_name)
      data = cur.execute(query, (count,)).fetchall()
    else: #count=None
      data = cur.execute("""SELECT * FROM {table} 
        ORDER by id DESC""".format(table=table_name)).fetchall()
    return data

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