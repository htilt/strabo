from datetime import datetime
from strabo import config_canyon

from sqlalchemy import *
import sqlalchemy
from sqlalchemy.orm import relationship

Base = sqlalchemy.ext.declarative.declarative_base()

class IdPrimaryKeyMixin:
    id = Column(Integer, primary_key=True)

class DateTimeMixin:
    created_at = Column(DateTime, default=datetime.now)

class DataType(IdPrimaryKeyMixin, DateTimeMixin):
    pass

class InterestPoints(Base,DataType):
    __tablename__ = 'interest_points'
    title = Column(Text)
    descrip_body = Column(Text)

    geojson_object = Column(Text)
    geojson_feature_type = Column(Text)

    # for some weird reason, enums break this and I cannot figure it out.
    layer = Column(Integer)

    images = relationship("Images",back_populates="interest_point")

class Images(Base,DataType):
    __tablename__ = 'images'
    filename = Column(Text)

    taken_at = Column(DateTime)

    interest_point_id = Column(Integer, ForeignKey('interest_points.id'))
    interest_point = relationship("InterestPoints",back_populates="images")

    description = Column(Text)

    #width and height in pixels, needed for photoswipe
    width = Column(Integer)
    height = Column(Integer)
