import os
from contextlib import closing

from strabo import app
from strabo import schema_livy
from strabo import db
from sqlalchemy.sql.expression import func

#converts a sqlalchemy object to a dictionary from strings
#that correspond to the collums of the table to the information in each
#collumn in the row
def obj_to_dict(obj):
    #kind of hackish solution that may not always work due to how sqlalchemy works
    return obj.__dict__

def obj_list_to_dict_list(objs):
    return [obj_to_dict(ob) for ob in objs]

# get the maximum id in table images
def get_max_img_id():
  data = db.session.query(func.max(schema_livy.Images.id)).one()
  maxid = data[0]
  return 0 if data == None else 0

# returns a number of row objects in the table table
def get_rows(table,count):
    return table.query.limit(count).all()

#return all result objects of the table
def get_all_rows(table):
    return table.query.all()

#searches all rows in Image tablesearch_term for search term
def search_all_image_fields(search_term):
    entries = []
    for col_name in app.config['IMAGE_SEARCH_COLUMNS']:
        entries += search(schema_livy.Images,col_name,search_term)
    return entries
    #start on a performance optimization on above that sends a single sql query instead of many
    '''
    search_cols = app.config['IMAGE_SEARCH_COLUMNS']
    search_col_objs = [table_column_name_dic[table.__table__.name][col_name] for col_name in search_cols]
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

def get_row_by_id(table,id):
    return obj_to_dict(table.query.get(id))

# searches for rows with search_term in column
def search_text(table, column, search_term):
    if not column in table.__table__.columns:
        return []
    column_obj = schema_livy.table_column_name_dic[table.__table__.name][column]

    if column in app.config['FUZZY_SEARCH_COLUMNS']:
        #returns all strings that have the search term as a substring/
        dataquery = table.query.filter(column_obj.like('%{}%'.format(search_term)))
    else:
        dataquery = table.query.filter(column_obj==search_term)

    datathing = dataquery.all()
    if not isinstance(datathing,list):
        datathing = [datathing]
    return obj_list_to_dict_list(datathing)

def delete_file(filename,file_path):
    file_fullpath = os.path.join(file_path, filename)
    os.remove(file_fullpath)

def delete_image_data(filename,thumbnail_name):
    delete_file(filename,app.config['UPLOAD_FOLDER'])
    delete_file(thumbnail_name,app.config['NEW_DATA_DIRECTORY'])

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

# Returns a list of dictionaries from collumn names to rows
# All rows in list are of a given feature type
def get_geojson(geojson_feature_type):
    ips = schema_livy.InterestPoints.query.filter_by(geojson_feature_type=geojson_feature_type).all()
    geodata = obj_list_to_dict_list(ips)
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
