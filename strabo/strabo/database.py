import os
from contextlib import closing

from strabo import app
from strabo import schema
from strabo import db
from sqlalchemy.sql.expression import func

def get_row_by_id(table,id):
    return table.query.get(id)

#delete helper functions
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
        if table is schema.Images:
            delete_image_data(keyrow.filename,keyrow.thumbnail_name)
        idquery.delete()
    db.session.commit()

# Returns a list of dictionaries from collumn names to rows
# All rows in list are of a given feature type
def get_geo_objects(geojson_feature_type):
    feature_ips = schema.InterestPoints.query.filter_by(geojson_feature_type=geojson_feature_type).all()
    obj_list = [ip.geojson_object for ip in feature_ips]
    return obj_list

#return all result objects of the table
def get_all_rows(table):
    return table.query.all()

def store_item(row_obj):
    db.session.add(row_obj)
    db.session.commit()
