'''
This file is here to help test strabo.

To use it, run add_database.py after the database has been initialized.

It adds interest points and images to the database, so you can see if features are working
without having to add ips and imgs yourself.
'''

import shutil
import os
import sys

from strabo import utils
import config
from strabo import schema
from strabo import private_helper

from strabo import db, app,straboconfig

def recreate_postgres_db():
    ''' Hackish and bad way of reinniting the postgres database
    by deleting the entire thing and starting over.
    only use for development.'''
    os.system("dropdb strabo")
    #deletes all files in folder specified except hidden files and those with no file extension.
    os.system("rm strabo/static/uploads/*$.*")
    os.system("rm strabo/static/thumbnails/*$.*")
    os.system("createdb strabo")
    os.system("python initDB.py")

# recreate_postgres_db()
class mock_flask_file_obj:
    '''
    Mocks the flask object that is in request.files.

    Has a ``filename`` attribute, which a theoretically arbitrary string.
        In this case corresponds the name of a real file.

    Has a ``save`` method that saves the file under a specified path.
        In this case

    :ivar filename: initial value: filename

        descript

    '''
    def __init__(self,path,filename):
        self.filename = filename
        #sys.path.append(os.path.realpath('../test_images/'))
        #path = sys.path[-1]
        self.full_filename = os.path.join(path,filename)

    def save(self,new_file_path):
        shutil.copyfile(self.full_filename,new_file_path)

def add_database():
    utils.fill_dict_with(straboconfig,config.get_config_info())

    geo_obj1 = '{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-122.63034939765929,45.48205499198348]}}'
    geo_obj2 = '{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-122.630397,45.481851]}}'
    geo_obj3 = '{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-122.63245,45.48236]}}'

    img1 = private_helper.make_image(1,"",mock_flask_file_obj("test_images","download.jpg"),"bird","1998","10")
    img2 = private_helper.make_image(2,"",mock_flask_file_obj("test_images","download1.jpg"),"flower","1989","10")
    img3 = private_helper.make_image(3,"",mock_flask_file_obj("test_images","download2.jpg"),"small flowers","1989","11")
    img4 = private_helper.make_image(4,"",mock_flask_file_obj("test_images","download3.jpg"),"beach","2010","10")
    img5 = private_helper.make_image(5,"",mock_flask_file_obj("test_images","image with space.jpg"),"canyon","1998","")
    img6 = private_helper.make_image(6,"",mock_flask_file_obj("test_images","phone_testing.png"),"phone","1997","11")
    img7 = private_helper.make_image(7,"",mock_flask_file_obj("test_images","FishLadder2001.jpg"),"Fish Ladder Construction, November 2001","2001","10")
    img8 = private_helper.make_image(8,"",mock_flask_file_obj("test_images","FishLadderSmallSize.jpg"),"Fish Ladder Today","2009","6")

    ip3_description = "Reed Lake was created sometime near the turn of the century by the construction of a 10-foot-high dam across Reed Creek. The creation of the dam blocked fish passage, as the creek was re-routed through a culvert system that discharged to a steep waterfall. \n \n Over the summer and fall of 2001, Reed College constructed a fish ladder to re-establish connectivity between Reed Lake and the lower creek for resident and anadromous fish."

    ip1 = private_helper.make_interest_point("",[img1,img2,img3,img6],"Interest Point 1","This is a descriptions of something",geo_obj1,"Plants","Navy")
    ip2 = private_helper.make_interest_point("",[img4,img5],"Interest Point 2","This is a descriptions of something else",geo_obj2,"Animals","Green")
    ip3 = private_helper.make_interest_point("",[img7,img8],"Fish Ladder",ip3_description,geo_obj3,"Interest Points","Green")

    db.session.add(ip1)
    db.session.add(ip2)
    db.session.add(ip3)

    db.session.commit()

if __name__=="__main__":
    add_database()
