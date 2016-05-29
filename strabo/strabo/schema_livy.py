from strabo import db
from datetime import datetime

import enum

class IdPrimaryKeyMixin(object):
    id = db.Column(db.Integer, primary_key=True)

class DateTimeMixin(object):
    created_at = db.Column(db.DateTime, default=datetime.now)

class DataType(IdPrimaryKeyMixin, DateTimeMixin):
    pass

class Images(db.Model,DataType):
    title = db.Column(db.Text)
    img_description = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    date_created = db.Column(db.Text)
    interest_point = db.Column(db.Text)
    event = db.Column(db.Text)
    period = db.Column(db.Text)
    notes = db.Column(db.Text)
    tags = db.Column(db.Text)
    edited_by = db.Column(db.Text)
    filename = db.Column(db.Text)
    thumbnail_name = db.Column(db.Text)

class Events(db.Model,DataType):
    title = db.Column(db.Text)
    event_description = db.Column(db.Text)
    date_of_event = db.Column(db.Text)
    notes = db.Column(db.Text)
    tags = db.Column(db.Text)
    edited_by = db.Column(db.Text)

class InterestPoints(db.Model,DataType):
    name = db.Column(db.Text)
    books = db.Column(db.Text)
    coordinates = db.Column(db.Text)
    geojson_object = db.Column(db.Text)
    feature_type = db.Column(db.Text)
    geojson_feature_type = db.Column(db.Text)
    notes = db.Column(db.Text)
    tags = db.Column(db.Text)
    edited_by = db.Column(db.Text)

class TextSelections(db.Model,DataType):
    name = db.Column(db.Text)
    book = db.Column(db.Text)
    section = db.Column(db.Text)
    pages = db.Column(db.Text)
    passage = db.Column(db.Text)
    interest_point = db.Column(db.Text)
    event = db.Column(db.Text)
    notes = db.Column(db.Text)
    tags = db.Column(db.Text)
    edited_by = db.Column(db.Text)

mdata = db.metadata
tables = mdata.sorted_tables
table_column_name_dic = {t.name:{e.name:e for e in t.columns} for t in mdata.sorted_tables}
table_column_names = {t.name:[e.name for e in t.columns] for t in mdata.sorted_tables}

'''
table_names = {t.name for t in mdata.sorted_tables}
class_names = {t.name:t for t in mdata.sorted_tables}
'''
