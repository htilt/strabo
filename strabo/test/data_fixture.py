import unittest
from strabo import db, app
from strabo import geojson_wrapper
from strabo import database
from strabo import image_processing
from strabo import schema
from strabo import utils
from strabo.config_canyon import Layers
from strabo import private_helper
import os
from strabo import app
from strabo import straboconfig
import shutil

app.config['SQLALCHEMY_DATABASE_URI']  = "sqlite:///../test_sqlalchemy_data.sqlite3"

class mock_flask_file_obj:
    def __init__(self,path,filename):
        self.filename = filename
        self.full_filename = os.path.join(path,filename)

    def save(self,new_file_path):
        shutil.copyfile(self.full_filename,new_file_path)


#hackish and bad way of reinniting the postgres database
def recreate_postgres_db():
    #delete database
    os.system("rm sqlalchemy_data.sqlite3")
    os.system("rm strabo/static/uploads/*")
    os.system("rm strabo/static/thumbnails/*")
    #recreates database
    os.system("python initDB.py")

class DatabaseFixture(unittest.TestCase):
    def setUp(self):
        geo_obj1 = '{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-122.63034939765929,45.48205499198348]}}'
        geo_obj2 = '{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-122.630397,45.481851]}}'

        ip1 = private_helper.make_interest_point("Interest Point 1","This is a descriptions of something",geo_obj1,"Plants")
        ip2 = private_helper.make_interest_point("Interest Point 2","This is a descriptions of something else",geo_obj2,"Animals")

        db.session.add(ip1)
        db.session.add(ip2)

        db.session.commit()

        img1 = private_helper.make_image(mock_flask_file_obj("test_images","download.jpg"),ip1.id)
        img2 = private_helper.make_image(mock_flask_file_obj("test_images","download1.jpg"),ip1.id)
        img3 = private_helper.make_image(mock_flask_file_obj("test_images","download2.jpg"),ip1.id)
        img4 = private_helper.make_image(mock_flask_file_obj("test_images","download3.jpg"),ip2.id)
        img5 = private_helper.make_image(mock_flask_file_obj("test_images","image with space.jpg"),ip2.id)
        img6 = private_helper.make_image(mock_flask_file_obj("test_images","phone_testing.png"),ip2.id)

        db.session.add(img1)
        db.session.add(img2)
        db.session.add(img3)
        db.session.add(img4)
        db.session.add(img5)
        db.session.add(img6)

        db.session.commit()

    def tearDown(self):
        recreate_postgres_db()
