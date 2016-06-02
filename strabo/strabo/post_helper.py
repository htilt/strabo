import werkzeug
import os
from strabo.image_processing import make_thumbnail, allowed_file
from strabo.geojson_wrapper import get_type, add_name_and_color

from strabo import app
from strabo import schema
from strabo import geojson_wrapper
from strabo import database

from strabo import image_processing
from strabo import utils

#makes an interest point from text input from the admin interface
def make_interest_point(form_title,form_body,form_geo_obj,form_layer):
    return schema.InterestPoints(
        title=form_title,
        descrip_body=form_body,
        geojson_object=geojson_wrapper.add_name_and_color(form_geo_obj,form_title),
        geojson_feature_type=str(geojson_wrapper.get_type(form_geo_obj)),
        layer=app.config['LAYER_FIELD_ENUMS'][form_layer].value
        )

#make image from flask file object
#saves image and thumbnail in static
#returns image database object
def make_image(form_file_obj,ip_id_str):
    #if no files is attached, then do nothing
    if not form_file_obj:
        return

    #if the file extension is not allowed,throw an error
    #todo: put this error in the frontend instead of here
    if not image_processing.allowed_file(form_file_obj.filename):
        raise RuntimeError("file extension not allowed")

    secure_filename = werkzeug.secure_filename(form_file_obj.filename)

    # prepend unique id to ensure an unique filename
    unique_filename = utils.unique_filename(app.config['UPLOAD_FOLDER'],secure_filename)
    # Move the file from the temporary folder to the upload folder
    form_file_obj.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
    # Make a thumbnail and store it in the thumbnails directory
    image_processing.make_thumbnail(unique_filename)

    ip_id = int(ip_id_str)
    return schema.Images(filename=unique_filename,interest_point=database.get_row_by_id(schema.InterestPoints,ip_id))
