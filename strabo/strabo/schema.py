from strabo import db
from datetime import datetime
from sqlalchemy.orm import relationship
from strabo import config_canyon

Column = db.Column

class IdPrimaryKeyMixin(object):
    id = Column(db.Integer, primary_key=True)

class DateTimeMixin(object):
    created_at = Column(db.DateTime, default=datetime.now)

class DataType(IdPrimaryKeyMixin, DateTimeMixin):
    pass

class InterestPoints(db.Model,DataType):
    __tablename__ = 'interest_points'
    title = Column(db.Text)
    descrip_body = Column(db.Text)

    geojson_object = Column(db.Text)
    geojson_feature_type = Column(db.Text)

    # for some weird reason, enums break this and I cannot figure it out.
    layer = Column(db.Integer)

    images = db.relationship("Images",back_populates="interest_point")

class Images(db.Model,DataType):
    __tablename__ = 'images'
    filename = Column(db.Text)

    interest_point_id = Column(db.Integer, db.ForeignKey('interest_points.id'))
    interest_point = db.relationship("InterestPoints",back_populates="images")

    description = Column(db.Text)

    #width and height in pixels, needed for photoswipe
    width = Column(db.Integer)
    height = Column(db.Integer)



'''
mdata = db.metadata
tables = mdata.sorted_tables
table_column_name_dic = {t.name:{e.name:e for e in t.columns} for t in mdata.sorted_tables}
table_column_names = {t.name:[e.name for e in t.columns] for t in mdata.sorted_tables}

table_names = {t.name for t in mdata.sorted_tables}
class_names = {t.name:t for t in mdata.sorted_tables}
'''
