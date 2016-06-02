from strabo import db, app
from strabo import geojson_wrapper
from strabo import database
from strabo import image_processing
from strabo import schema
from strabo import utils
from strabo.config_canyon import Layers
import shutil
import werkzeug
import os

#hackish and bad way of reinniting the postgres database
def recreate_postgres_db():
    os.system("dropdb strabo_test")
    os.system("rm strabo/static/uploads/*")
    os.system("rm strabo/static/thumbnails/*")
    os.system("createdb strabo_test")
    os.system("python initDB.py")

recreate_postgres_db()


#makes an interest point from input from the admin interface
def make_interest_point(form_title,form_body,form_geo_obj,form_layer):
    return schema.InterestPoints(
        title=form_title,
        descrip_body=form_body,
        geojson_object=geojson_wrapper.add_name_and_color(form_geo_obj,form_title),
        geojson_feature_type=str(geojson_wrapper.get_type(form_geo_obj)),
        layer=app.config['LAYER_FIELD_ENUMS'][form_layer].value
        )

class mock_flask_file_obj:
    def __init__(self,path,filename):
        self.filename = filename
        self.full_filename = os.path.join(path,filename)

    def save(self,new_file_path):
        shutil.copyfile(self.full_filename,new_file_path)

def make_image(form_file_obj):
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
    thumb_name = image_processing.make_thumbnail(unique_filename)
    f_name = unique_filename

    return schema.Images(filename=f_name)

geo_obj1 = '{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-122.63034939765929,45.48205499198348]}}'
geo_obj2 = '{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-122.630397,45.481851]}}'

ip1 = make_interest_point("Interest Point 1","This is a descriptions of something",geo_obj1,app.config['LAYER_FIELDS'][Layers.plant])
ip2 = make_interest_point("Interest Point 2","This is a descriptions of something else",geo_obj2,app.config['LAYER_FIELDS'][Layers.animal])

img1 = make_image(mock_flask_file_obj("test_images","download.jpg"))
img2 = make_image(mock_flask_file_obj("test_images","download1.jpg"))
img3 = make_image(mock_flask_file_obj("test_images","download2.jpg"))
img4 = make_image(mock_flask_file_obj("test_images","download3.jpg"))
img5 = make_image(mock_flask_file_obj("test_images","image with space.jpg"))
img6 = make_image(mock_flask_file_obj("test_images","phone_testing.png"))

ip1.images.append(img1)
ip1.images.append(img2)
ip1.images.append(img3)
ip2.images.append(img4)
ip2.images.append(img5)
ip2.images.append(img6)

db.session.add(ip1)
db.session.add(ip2)

db.session.commit()
