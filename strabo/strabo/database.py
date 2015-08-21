import sqlite3, os
from contextlib import closing

from strabo import app

# This function starts a new connection to the bbs.sqlite3 database.
def get_db():
  conn = sqlite3.connect("bbs.sqlite3")
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

# return the total number of images in the db
def count_all_images(column=None, search_term=None):
  # count all images
  if column == None:
    query = """SELECT COUNT(*) FROM images"""
    image_count = simple_query(query)
  # count all images where column = search_term
  else:
    if column == 'date_created':
      query = """SELECT COUNT(*) FROM images 
      WHERE strftime('%Y', date_created) = ?"""
    else:
      query = """SELECT COUNT(*) FROM images 
      WHERE {column} = ?""".format(column=column)
    image_count = simple_query(query, (search_term,))
  return image_count[0]['COUNT(*)']

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

# This function ensures that get_images_helper will receive a safe 
# column name.
def get_images(year=None, event=None, location=None):
  if year is not None:
    return get_images_helper('date_created', year, 12)
  if event is not None:
    return get_images_helper('event', event, 12)
  else:
    return get_images_helper('interest_point', location, 12)

# Gets 12 images from db for which a given column matches the user input.
def get_images_helper(column, variable, count):
  if column == 'date_created':
    query = """SELECT * FROM images WHERE strftime('%Y', date_created) = ? 
      ORDER by id LIMIT ?"""
  else:
    query = """SELECT * FROM images WHERE {column} LIKE ? 
      ORDER by id LIMIT ?""".format(column = column)
  images = simple_query(query, (variable, count))
  return images

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
  'boolean': ['AND', 'OR']
}

# searches for rows with search_term in column
def search(table_name, column, search_term, count=None):
  if not table_name in SCHEMA:
    return []
  if not column in SCHEMA[table_name]:
    return []
  # if searching a lengthy text field, do fuzzy search
  if column in ("title", "img_description", "event_description", "name"):
    query = """SELECT * FROM {table} WHERE {column} LIKE ?
      ORDER BY id DESC""".format(table=table_name, column=column)
    search_term = '%{}%'.format(search_term)
    params = (search_term,)
  # otherwise, perform nromal search
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
      # if images is the table to be modified, delete the image from /uploads
      if table_name == "images":
        query = """SELECT filename FROM images WHERE id = ?"""
        file_name = simple_query(query, (key,))
        file_name = (file_name[0][0])
        path = app.config['UPLOAD_FOLDER']
        fullpath = os.path.join(path, file_name)
        os.remove(fullpath)
      # then delete the db row
      query = """DELETE FROM {table} WHERE id = ?""".format(table=table_name)
      db.execute(query, (key,))
    db.commit()
  return

# inserts an image into the db
def insert_images(params):
  with closing(get_db()) as db:
    db.cursor().execute("""INSERT INTO images(title, img_description, 
      latitude, longitude, date_created, interest_point, event, notes, 
      tags, edited_by, filename, thumbnail_name) VALUES(?, ?, ?, ?, ?, ?,
      ?, ?, ?, ?, ?, ?)""", params)
    db.commit()

# inserts an interest point into the db
def insert_ips(params):
  with closing(get_db()) as db:
    db.cursor().execute("""INSERT INTO interest_points
      (name, coordinates, geojson_object, feature_type, geojson_feature_type, 
        notes, tags, edited_by) VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", params)
    db.commit()

# inserts an event into the db
def insert_events(params):
  with closing(get_db()) as db:
    db.cursor().execute("""INSERT INTO events
      (title, event_description, date_of_event, notes, tags, edited_by) 
      VALUES(?, ?, ?, ?, ?, ?)""", params)
    db.commit()

# insert into all 14 columns in images to replace
def edit_image(params):
  with closing(get_db()) as db:
    db.cursor().execute("""REPLACE INTO images VALUES(?, ?, ?, ?, ?, ?, ?, 
      ?, ?, ?, ?, ?, ?, ?)""", params)
    db.commit()

# insert into all 10 columns in interest_points to replace
def edit_ip(params):
  with closing(get_db()) as db:
    db.cursor().execute("""REPLACE INTO interest_points VALUES(?, ?, ?, ?, ?, 
      ?, ?, ?, ?, ?)""", params)
    db.commit()

# insert into all 8 columns in events to replace
def edit_event(params):
  with closing(get_db()) as db:
    db.cursor().execute("""REPLACE INTO events VALUES(?, ?, ?, ?, ?, ?,
      ?, ?)""", params)
    db.commit()

# returns the geojson objects of a given feature type
def get_geojson(geojson_feature_type):
  query = """SELECT * FROM interest_points WHERE geojson_feature_type = ?"""
  geojson = simple_query(query, (geojson_feature_type,))
  return geojson

def get_images_for_page(id_num=None, page_event=None, search_criteria=None):
  # if no search term or column is provided
  print(search_criteria)
  if len(search_criteria) == 0:
    if page_event == 'next':
      query = """SELECT * FROM images WHERE id > ? ORDER BY id LIMIT 12"""
      params = (id_num,)
    elif page_event == 'previous':
      query = """SELECT * FROM images WHERE id < ? ORDER BY id DESC LIMIT 12"""
      params = (id_num,)
    else: 
      query = """SELECT * FROM images ORDER BY id LIMIT 12"""
      return simple_query(query)
  # if user is searching for images by an arbitrary column/search term
  else:
    # Make a string containing the user's query
    if page_event == 'next':
      query = """SELECT * FROM images WHERE id > ? AND """
      params = [id_num]      
    elif page_event == "previous":
      query = """SELECT * FROM images WHERE id < ? AND """
      params = [id_num]
    else: # page_event == None
      query = """SELECT * FROM images WHERE """
      params = []
    for tup in search_criteria:
      # if the tuple contains a column/search term pair
      if len(tup) == 2:
        # make the column
        column = tup[0]
        # ensure that the column name is in the schema
        # if not column in ('event', 'interest_point', 
        #   'strftime(\'%Y\', date_created'):
        #   return []
        # append a where clause to the query
        query = query + """{column} = ? """.format(column=column)
        # make the search term
        search_term = tup[1]
        # add the search term to the params
        params.append(search_term)
      # if the tuple contains a boolean
      elif len(tup) == 1:
        # get the boolean from the tuple
        boolean = tup[0]
        # ensure that the boolean is in the schema
        # if not boolean in ('AND', 'OR'):
        #   return []
        # append the boolean to the query
        query = query + """{boolean} """.format(boolean=boolean)
    params = tuple(params)
    # finish the query string
    query = query + """ ORDER BY id """
    if page_event == "previous": query = query + """DESC """
    query = query + """LIMIT 12"""
    print(query)
    print(params)
  images = simple_query(query, params)
  return images

