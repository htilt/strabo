'''
Assigns entries in the table accoring to text input from the admin interface.
'''
import werkzeug
import os
import datetime

from strabo import schema
from strabo import image_processing
from strabo import utils
from strabo import file_writing

from strabo import app
from strabo import db
from strabo import straboconfig

def fill_interest_point(ip,image_ids,form_title,form_body,form_geo_obj,form_layer,form_icon):
    if not ip.id:
        raise RuntimeError("ip needs to be stored in database to be filled")
    ip.title = form_title
    ip.descrip_body = form_body
    ip.geojson_object = form_geo_obj
    ip.layer = straboconfig["REVERSE_LAYER_FIELDS"][form_layer]
    ip.icon = form_icon
    ip.images = [db.session.query(schema.Images).get(int(id)) for id in image_ids]

def make_date(form_year,form_month):
    '''
    :param string form_year: Year value passed in from form. Is a string decimal
        representation of a year or en empty string if that part of the form was
        left empty.

    :param string form_month: Month value, follows same format as year.

    If month and year are valid values,returns a date with specied month and year.

    If not, then it uses today's date as a default.
    '''
    default_day = 1
    year = int(form_year) if form_year else datetime.date.today().year
    month = int(form_month) if form_month else datetime.date.today().month

    return  datetime.date(year,month,default_day)

def fill_image(image,form_file_obj,form_descrip,year,month):
    '''
    if a flask.files object is passed in, then
    '''
    image.taken_at = make_date(year,month)
    image.description = form_descrip

    if form_file_obj:
        image.filename = file_writing.make_filename(form_file_obj.filename)
        file_writing.save_image_files(form_file_obj,image.filename)
        image.width,image.height = image_processing.get_dimentions(image.filename)
