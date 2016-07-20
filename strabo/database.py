'''
Currently only handles interest poing and image deletion.

In future versions, this will handle all database interactions,
including gets, sets, updates.
'''

import os
import sqlalchemy

from strabo import schema
from strabo import file_writing

from strabo import app
from strabo import db

def delete_ip(id):
    '''Deletes ip refrenced by id.

    All images associated with the ip are unaffected, they simply lose their connection with the interest_point.'''
    idquery = db.session.query(schema.InterestPoints).filter_by(id=id)
    ip = idquery.one()

    ip.images = []#clears image ForeignKeys
    db.session.commit()

    idquery.delete()
    db.session.commit()

def delete_image(id):
    '''Deletes the images and all files associated with it.'''
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
