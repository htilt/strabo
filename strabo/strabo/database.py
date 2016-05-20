import os
from contextlib import closing

from strabo import app
from strabo import schema_livy
from strabo import db

#engine = sqlalchemy.create_engine(app.config['DATABASE_URL'], echo=app.config['IS_DEBUG'])

#Session = sessionmaker(bind=engine)

# get the maximum id in table images
def get_max_id():
  return session.query(func.max(Player.score)).one()

def get_flex(table, count=None):
    query = table.query
    if count == None:
        return query.all()
    else:
        return query.limit(count).all()

# Gets 10 images with select metadata
def get_flexold(table_name, count=None):
  if count:
    query = """SELECT * FROM {table} ORDER BY id DESC
      LIMIT ?""".format(table=table_name)
    data = simple_query(query, (count,))
  else: #count=None
    query = """SELECT * FROM {table}
      ORDER by id DESC""".format(table=table_name)
    data = simple_query(query)
  return data

def search_all_image_fields(search_term):
    entries = []
    for col_name in app.config['IMAGE_SEARCH_COLUMNS']:
        entries += search(schema_livy.Images,col_name,search_term)
    return entries
    #start on a performance optimization on above that sends a single sql query instead of many
    '''
    search_cols = app.config['IMAGE_SEARCH_COLUMNS']
    search_col_objs = [table_column_name_dic[table.name][col_name] for col_name in search_cols]
    if len(search_cols) == 0:
        return []
    else if len(search_cols) == 1:
        filter_obj = search_col_objs[0].like('%{}%'.format(search_term))
    else:
        filter_obj = db.or_(search_col_objs[0].like('%{}%'.format(search_term)),
                            search_col_objs[1].like('%{}%'.format(search_term)))
        for sc in search_cols[2:]:
            filter_obj = db.or_(filter_obj,sc.like('%{}%'.format(search_term)))
    curobj = db.or_()
    for col_name in search_cols[2:]:'''


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
  data = simple_query(query, paramsdic)
  return data

# searches for rows with search_term in column
def search(table, column, search_term):
    if not column in table.columns:
        return []
    column_obj = table_column_name_dic[table.name][column]
    # if searching a lengthy text field, do fuzzy search
    if column in app.config['FUZZY_SEARCH_COLUMNS']:
        dataquery = table.query.filter(column_obj.like('%{}%'.format(search_term)))
    else:
        dataquery = table.query.filter(column_obj==search_term)

    return dataquery.all()


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
      query = """ SELECT * FROM {table} WHERE {column} = ?
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
def delete(keys,table):
    for key in keys:
        idquery = table.query.filter(table.id == key)
        keyrow = idquery.one()
        if table is schema_livy.Images:
            delete_image_data(keyrow.filename,keyrow.thumbnail_name)
        idquery.delete()
    db.session.commit()

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
    geodata = InterestPoints.query.filter_by(geojson_feature_type=geojson_feature_type).all()
    print(geodata)
    return geodata

# inserts row entry with collums specified by the dictionary "params"
# into the sqlalchemy Table specified by table_type
def add_to_table(table_type,params):
    db.session.add(table_type(**params))
    db.session.commit()


# updates row entry in the sqlalchemy Table specified by table_type
# with id = key to match dictionary params
def edit_table_key(table_type,key,params):
    table_type.query.filter_by(id=key).update(params)
    db.session.commit()
