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
	notes = Column(Text)
	tags = Column(Text)
	edited_by = Column(Text)


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
    filename = Column(Text)
    thumbnail_name = Column(Text)


class Events(Base,DataType):
    __tablename__ = 'events'
    name = Column(Text)
    books = Column(Text)
    coordinates = Column(Text)
    geojson_object = Column(Text)
    feature_type = Column(Text)
    geojson_feature_type = Column(Text)

class TextSelections(Base,DataType):
    __tablename__ = 'text_selections'
    name = Column(Text)
    book = Column(Text)
    section = Column(Text)
    pages = Column(Text)
    passage = Column(Text)
    interest_point = Column(Text)
    event = Column(Text)
