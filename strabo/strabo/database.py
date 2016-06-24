import os
from contextlib import closing

from strabo import app
from strabo import db
from strabo import schema
import sqlalchemy

engine = sqlalchemy.create_engine(app.config["SQLALCHEMY_DATABASE_URI"], echo=app.config['DEBUG'])

get_session = sqlalchemy.orm.sessionmaker(bind=engine)

def get_row_by_id(table,id):
    return db.session.query(table).get(id)

#deletes ip refrenced by id and clears the relationships it has with images
def delete_ip(id):
    idquery = db.session.query(schema.InterestPoints).filter_by(id=id)
    ip = idquery.one()

    ip.images = []#clears image ForeignKeys
    db.session.commit()

    idquery.delete()
    db.session.commit()

#delete image helper functions
def delete_file(filename,file_path):
    file_fullpath = os.path.join(file_path, filename)
    os.remove(file_fullpath)

def delete_image_data(filename,thumbnail_name):
    delete_file(filename,app.config['UPLOAD_FOLDER'])
    delete_file(thumbnail_name,app.config['NEW_DATA_DIRECTORY'])

#deletes the images and the uploaded file associated
def delete_image(id):
    idquery = db.session.query(schema.Images).filter_by(id=id)
    img = idquery.one()
    delete_image_data(img.filename,img.filename)
    idquery.delete()
    db.session.commit()

# Returns a list of dictionaries from collumn names to rows
# All rows in list are of a given feature type
def get_geo_objects(geojson_feature_type):
    feature_ips = db.session.query(schema.InterestPoints).filter_by(geojson_feature_type=geojson_feature_type).all()
    obj_list = [ip.geojson_object for ip in feature_ips]
    return obj_list

#return all result objects of the table
def get_all_rows(table):
    return db.session.query(table).all()

def store_item(row_obj):
    db.session.add(row_obj)
    db.session.commit()
