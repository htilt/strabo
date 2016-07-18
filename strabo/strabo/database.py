import os
import sqlalchemy

from strabo import schema
from strabo import file_writing

from strabo import app
from strabo import db

#deletes ip refrenced by id and clears the relationships it has with images
def delete_ip(id):
    idquery = db.session.query(schema.InterestPoints).filter_by(id=id)
    ip = idquery.one()

    ip.images = []#clears image ForeignKeys
    db.session.commit()

    idquery.delete()
    db.session.commit()

#deletes the images and the uploaded file associated
def delete_image(id):
    idquery = db.session.query(schema.Images).filter_by(id=id)
    img = idquery.one()
    file_writing.delete_image_files(img.filename)
    idquery.delete()
    db.session.commit()

#helper functions, currently unused
'''
def get_row_by_id(table,id):
    return db.session.query(table).get(id)

#return all result objects of the table
def get_all_rows(table):
    return db.session.query(table).all()

def store_item(row_obj):
    db.session.add(row_obj)
    db.session.commit()
'''
