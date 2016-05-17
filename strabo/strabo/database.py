import os
from contextlib import closing

from strabo import app
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from strabo import schema_livy
from strabo import app

engine = sqlalchemy.create_engine(app.config['DATABASE_URL'], echo=app.config['IS_DEBUG'])

Session = sessionmaker(bind=engine)

def new_session():
    return Session()

# get the maximum id in table images
def get_max_id():
  return session.query(func.max(Player.score)).one()

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
'''SCHEMA = {
  'images': [c[0] for c in get_column_names('images')],
  'events': [c[0] for c in get_column_names('events')],
  'interest_points': [c[0] for c in get_column_names('interest_points')],
  'text_selections': [c[0] for c in get_column_names('text_selections')],
  'boolean': ['AND', 'OR']
}'''

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
    if (not table_name in schema_livy.table_names or
            not column in schema_livy.table_collums[table_name]):
        return []
    session = Session()
    sqltable = session.query(schema_livy.class_names[table_name])
    # if searching a lengthy text field, do fuzzy search
    if column in ("title", "img_description", "event_description", "name",
        "passage", "tags", "notes"):
        sqltable.filter()

def searchold(table_name, column, search_term, count=None):
  if (not table_name in schema_livy.table_names or
        not column in schema_livy.table_collums[table_name]):
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

def delete_file(filename,file_path):
    file_fullpath = os.path.join(file_path, filename)
    os.remove(file_fullpath)

def delete_image_data(filename,thumbnail_name):
    delete_file(filename,app.config['UPLOAD_FOLDER'])
    delete_file(thumbnail_name,app.config['NEW_DATA_DIRECTORY'])

# SEARCH_VAR_PATTERN = re.compile(r'^[\w_]+$')

# receives a list of ids and loops over them, deleting
# each row from the db. If an image is deleted, the function also
# removes the image file from /uploads
def delete(keys,table_name):
    if table_name not in schema_livy.table_names:
        return []

    table_type = schema_livy.class_names[table_name]

    session = Session()
    sqltable = session.query(table_type)
    for key in keys:
        keyrow = sqltable.filter(table_type.id == id)
        if table_name == "images":
            delete_image_data(keyrow.filename,keyrow.thumbnail_name)
        session.delete(keyrow)
    session.commit()

def deleteold(keys, table_name):
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
    ses = Session()
    geodata = ses.query().filter(InterestPoints.geojson_feature_type == geojson_feature_type)
    print(geodata)
    return geodata

def param_add_fn(table_type):
    def calc(params):
        ses = Session()
        ses.add(schema_livy.Images(**params))
        ses.commit()
    return calc

# inserts an image into the db
insert_images = param_add_fn(schema_livy.Images)

# inserts an interest point into the db
insert_ips = param_add_fn(schema_livy.InterestPoints)

# inserts an event into the db
insert_ips = param_add_fn(schema_livy.Events)

# inserts an event into the db
insert_ips = param_add_fn(schema_livy.TextSelections)

def param_edit_fn(table_type):
    def calc(id,params):
        ses = Session()
        ses.query(table_type).filter(table_type.id == id).update(**params)
        ses.commit()
    return calc

#replace all params in the image specified by the id
edit_image = param_edit_fn(schema_livy.Images)

#replace all params in the interest point specified by the id
edit_ip = param_edit_fn(schema_livy.InterestPoints)

#replace all params in the event specified by the id
edit_event = param_edit_fn(schema_livy.Events)

#replace all params in the test selection specified by the id
edit_textselection = param_edit_fn(schema_livy.TextSelections)
