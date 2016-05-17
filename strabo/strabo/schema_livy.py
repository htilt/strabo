from datetime import datetime

from sqlalchemy import (Column, Integer, String,
                        DateTime, Text, ForeignKey, Enum,Float)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import sqlalchemy

import enum

Base = declarative_base()


class IdPrimaryKeyMixin(object):
    id = Column(Integer, primary_key=True)

class DateTimeMixin(object):
    created_at = Column(DateTime, default=datetime.now)

class DataType(IdPrimaryKeyMixin, DateTimeMixin):
    pass

class Images(Base,DataType):
    __tablename__ = 'images'
    title = Column(Text)
    img_description = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    date_created = Column(Text)
    interest_point = Column(Text)
    event = Column(Text)
    period = Column(Text)
    notes = Column(Text)
    tags = Column(Text)
    edited_by = Column(Text)
    filename = Column(Text)
    thumbnail_name = Column(Text)

class Events(Base,DataType):
    __tablename__ = 'events'
    title = Column(Text)
    event_description = Column(Text)
    date_of_event = Column(Text)
    notes = Column(Text)
    tags = Column(Text)
    edited_by = Column(Text)

class InterestPoints(Base,DataType):
    __tablename__ = 'interest_points'
    name = Column(Text)
    books = Column(Text)
    coordinates = Column(Text)
    geojson_object = Column(Text)
    feature_type = Column(Text)
    geojson_feature_type = Column(Text)
    notes = Column(Text)
    tags = Column(Text)
    edited_by = Column(Text)

class TextSelections(Base,DataType):
    __tablename__ = 'text_selections'
    name = Column(Text)
    book = Column(Text)
    section = Column(Text)
    pages = Column(Text)
    passage = Column(Text)
    interest_point = Column(Text)
    event = Column(Text)
    notes = Column(Text)
    tags = Column(Text)
    edited_by = Column(Text)

mdata = Base.metadata
table_names = {t.name for t in mdata.sorted_tables}
table_collums = {t.name:{e.name for e in t.columns} for t in mdata.sorted_tables}
class_names = {t.name:t for t in mdata.sorted_tables}
#print(table_names,"\n\n")
#print()
