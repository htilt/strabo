import werkzeug
import os
import datetime
from strabo import image_processing

from strabo import app
from strabo import schema
from strabo import geojson_wrapper
from strabo import database
from strabo import db

from strabo import image_processing
from strabo import utils

#assigns entries in the InterestPoints accoring to text input from the admin interface
#requires theadd_name_and_color
def fill_interest_point(ip,image_ids,form_title,form_body,form_geo_obj,form_layer):
    if not ip.id:
        raise RuntimeError("ip needs to be stored in database to be filled")
    ip.title = form_title
    ip.descrip_body = form_body
    ip.geojson_object = geojson_wrapper.add_info(form_geo_obj,form_title,ip.id)
    ip.geojson_feature_type = str(geojson_wrapper.get_type(form_geo_obj))
    ip.layer = app.config['LAYER_FIELD_ENUMS'][form_layer].value
    ip.images = [db.session.query(schema.Images).get(int(id)) for id in image_ids]

#saves image and thumbnail using the given filenaem
def save_image(form_file_obj,filename):
    #if no files is attached, then do nothing
    if not form_file_obj:
        return
    #if the file extension is not allowed,throw an error
    #todo: put this error in the frontend instead of here
    if not image_processing.allowed_file(form_file_obj.filename):
        raise RuntimeError("file extension not allowed")

    # Move the file from the temporary folder to the upload folder
    form_file_obj.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # Make a thumbnail and store it in the thumbnails directory with the same filename
    # will also be unique as there will be the same files in both
    image_processing.make_thumbnail(filename,filename)

#gives a safe filename that is not the same as any other in the uploads folder
def make_filename(form_file_name):
    secure_filename = werkzeug.secure_filename(form_file_name)
    # prepend unique id to ensure an unique filename
    unique_filename = utils.unique_filename(app.config['UPLOAD_FOLDER'],secure_filename)
    return  unique_filename

def fill_image(image,form_file_obj,form_descrip,year,month,day):
    image.taken_at = datetime.date(utils.safe_pos_int_conv(year),utils.safe_pos_int_conv(month),utils.safe_pos_int_conv(day))
    image.description = form_descrip

    if form_file_obj:
        image.filename = make_filename(form_file_obj.filename)
        save_image(form_file_obj,image.filename)
        image.width,image.height = image_processing.get_dimentions(image.filename)
