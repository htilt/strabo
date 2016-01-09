import sqlite3, os
from contextlib import closing

from strabo import app

# This function starts a new connection to the bbs.sqlite3 database.
def get_db():
  conn = sqlite3.connect(app.config['DATABASE'])
  return conn

# get the maximum id in table images
def get_max_id():
  with closing(get_db()) as db:
    cur = db.cursor()
    cur = cur.execute('SELECT max(id) FROM images')
    max_id = cur.fetchone()[0]
    if max_id == None:
      max_id = 0
  return max_id

# given a query and parameters, perform the query
def simple_query(query, params=None):
  with closing(get_db()) as db:
    db.row_factory = dict_factory
    cur = db.cursor()
    if params == None:
      data = cur.execute(query).fetchall()
    else:
      data = cur.execute(query, params).fetchall()
  return data

# returns sqlite results as dictionaries, with column names
# that can be referenced
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Gets 10 images with select metadata
def get_flex(table_name, count=None):
  if count:
    query = """SELECT * FROM {table} ORDER BY id DESC 
      LIMIT ?""".format(table=table_name)
    data = simple_query(query, (count,))
  else: #count=None
    query = """SELECT * FROM {table} 
      ORDER by id DESC""".format(table=table_name)
    data = simple_query(query)
  return data

# Gets column names from a given table
def get_column_names(table_name):
  with closing(get_db()) as db:
    c = db.cursor()
    c.execute('SELECT * FROM {table}'.format(table=table_name))
    column_names = c.description
  return column_names

# define accepted terms for the schema
SCHEMA = {
  'images': [c[0] for c in get_column_names('images')],
  'events': [c[0] for c in get_column_names('events')],
  'interest_points': [c[0] for c in get_column_names('interest_points')],
  'text_selections': [c[0] for c in get_column_names('text_selections')],
  'boolean': ['AND', 'OR']
}

# searches for rows with search_term in specified column or in multiple columns
# with fuzzy search
def gallery_search(table_name, search_term, column=None):
  if not table_name in SCHEMA:
    return []
  if not column in SCHEMA[table_name] and not column == None:
    return []
  # do fuzzy search
  if column == None:
    query = """SELECT * FROM {table} WHERE title LIKE ? OR img_description LIKE ?
      OR interest_point LIKE ? OR event LIKE ? OR notes LIKE ? ORDER BY id 
      DESC""".format(table=table_name)
    search_term = '%{}%'.format(search_term)
    params = (search_term,search_term,search_term,search_term,search_term)
  else:
    query = """SELECT * FROM {table} WHERE {column} LIKE ?
      ORDER BY id DESC""".format(table=table_name, column=column)
    search_term = '%{}%'.format(search_term)
    params = (search_term,)
  data = simple_query(query, params)
  return data

# searches for rows with search_term in column
def search(table_name, column, search_term, count=None):
  if not table_name in SCHEMA:
    return []
  if not column in SCHEMA[table_name]:
    return []
  # if searching a lengthy text field, do fuzzy search
  if column in ("title", "img_description", "event_description", "name", 
    "passage", "tags", "notes"):
    query = """SELECT * FROM {table} WHERE {column} LIKE ?
      ORDER BY id DESC""".format(table=table_name, column=column)
    search_term = '%{}%'.format(search_term)
    params = (search_term,)
  # otherwise, perform normal search
  else:
    if count != None:
      query = """SELECT * FROM {table} WHERE {column} = ?
        ORDER by id DESC LIMIT ?""".format(table=table_name, column=column)
      params = (search_term, count)
    else:
      query = """SELECT * FROM {table} WHERE {column} = ?
        ORDER by id DESC""".format(table=table_name, column=column)
      params = (search_term,)
  data = simple_query(query, params)
  return data

# SEARCH_VAR_PATTERN = re.compile(r'^[\w_]+$')

# receives a list of ids and loops over them, deleting 
# each row from the db. If an image is deleted, the function also
# removes the image file from /uploads
def delete(keys, table_name):
  if not table_name in SCHEMA:
    return []
  with closing(get_db()) as db:
    c = db.cursor()
    for key in keys:
      # if images is the table to be modified, 
      if table_name == "images":
        query1 = """SELECT filename FROM images WHERE id = ?"""
        query2 = """SELECT thumbnail_name FROM images WHERE id = ?"""
        # get the filename
        file_name = simple_query(query1, (key,))
        file_name = (file_name[0]['filename'])
        # get the thumbnail name
        thumbnail_name = simple_query(query2, (key,))
        thumbnail_name = (thumbnail_name[0]['thumbnail_name'])

        # delete the image from /uploads
        file_path = app.config['UPLOAD_FOLDER']
        file_fullpath = os.path.join(file_path, file_name)
        os.remove(file_fullpath)
        # then delete the image from /thumbnails
        thumbnail_path = app.config['NEW_DATA_DIRECTORY']
        thumbnail_fullpath = os.path.join(thumbnail_path, thumbnail_name)
        os.remove(thumbnail_fullpath)
      # then delete the db row
      query = """DELETE FROM {table} WHERE id = ?""".format(table=table_name)
      db.execute(query, (key,))
    db.commit()
  return

# returns the geojson objects of a given feature type
def get_geojson(geojson_feature_type):
  query = """SELECT * FROM interest_points WHERE geojson_feature_type = ?"""
  geojson = simple_query(query, (geojson_feature_type,))
  print(geojson)
  return geojson

# inserts an image into the db
def insert_images(params):
  with closing(get_db()) as db:
    query = app.config['INSERT_IMG_QUERY']
    db.cursor().execute(query, params)
    db.commit()

# inserts an interest point into the db
def insert_ips(params):
  with closing(get_db()) as db:
    query = app.config['INSERT_IP_QUERY']
    db.cursor().execute(query, params)
    db.commit()

# inserts an event into the db
def insert_events(params):
  with closing(get_db()) as db:
    query = app.config['INSERT_EVENT_QUERY']
    db.cursor().execute(query, params)
    db.commit()

# inserts an event into the db
def insert_text(params):
  with closing(get_db()) as db:
    query = app.config['INSERT_TEXT_QUERY']
    db.cursor().execute(query, params)
    db.commit()

# insert into all 14 columns in images to replace
def edit_image(params):
  with closing(get_db()) as db:
    query = app.config['EDIT_IMG_QUERY']
    db.cursor().execute(query, params)
    db.commit()

# insert into all 10 columns in interest_points to replace
def edit_ip(params):
  with closing(get_db()) as db:
    query = app.config['EDIT_IP_QUERY']
    db.cursor().execute(query, params)
    db.commit()

# insert into all 8 columns in events to replace
def edit_event(params):
  with closing(get_db()) as db:
    query = app.config['EDIT_EVENT_QUERY']
    db.cursor().execute(query, params)
    db.commit()

# insert into all 12 columns in text_selections to replace
def edit_textselection(params):
  with closing(get_db()) as db:
    query = app.config['EDIT_TEXT_QUERY']
    db.cursor().execute(query, params)
    db.commit()



