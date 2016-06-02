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
#only use for development
def recreate_postgres_db():
    os.system("dropdb strabo_test")
    os.system("rm strabo/static/uploads/*")
    os.system("rm strabo/static/thumbnails/*")
    os.system("createdb strabo_test")
    os.system("python initDB.py")

recreate_postgres_db()

class mock_flask_file_obj:
    def __init__(self,path,filename):
        self.filename = filename
        self.full_filename = os.path.join(path,filename)

    def save(self,new_file_path):
        shutil.copyfile(self.full_filename,new_file_path)


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