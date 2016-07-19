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

utils.fill_dict_with(straboconfig,config.get_config_info())

def recreate_postgres_db():
    ''' hackish and bad way of reinniting the postgres database
     only use for development'''
    os.system("dropdb strabo")
    os.system("rm strabo/static/uploads/*.*")
    os.system("rm strabo/static/thumbnails/*.*")
    os.system("createdb strabo")
    os.system("python initDB.py")

# recreate_postgres_db()
class mock_flask_file_obj:
    '''
    Mocks the flask object that is in request.files.
    '''
    def __init__(self,path,filename):
        self.filename = filename
        #sys.path.append(os.path.realpath('../test_images/'))
        #path = sys.path[-1]
        self.full_filename = os.path.join(path,filename)

    def save(self,new_file_path):
        shutil.copyfile(self.full_filename,new_file_path)

def make_interest_point(image_ids,form_title,form_body,form_geo_obj,form_layer,form_icon):
    ip = schema.InterestPoints()
    db.session.add(ip)
    db.session.flush()
    private_helper.fill_interest_point(ip,image_ids,form_title,form_body,form_geo_obj,form_layer,form_icon)
    db.session.commit()
    return ip

#returns image database object
def make_image(form_file_obj,form_descrip,year,month,day):
    img = schema.Images()
    private_helper.fill_image(img,form_file_obj,form_descrip,year,month,day)
    return img

geo_obj1 = '{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-122.63034939765929,45.48205499198348]}}'
geo_obj2 = '{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-122.630397,45.481851]}}'
geo_obj3 = '{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-122.63245,45.48236]}}'


img1 = make_image(mock_flask_file_obj("test_images","download.jpg"),"bird","1998","10","1")
img2 = make_image(mock_flask_file_obj("test_images","download1.jpg"),"flower","1989","10","11")
img3 = make_image(mock_flask_file_obj("test_images","download2.jpg"),"small flowers","1989","11","")
img4 = make_image(mock_flask_file_obj("test_images","download3.jpg"),"beach","201","10","12")
img5 = make_image(mock_flask_file_obj("test_images","image with space.jpg"),"canyon","1998","","1")
img6 = make_image(mock_flask_file_obj("test_images","phone_testing.png"),"phone","1997","11","12")
img7 = make_image(mock_flask_file_obj("test_images","FishLadder2001.jpg"),"Fish Ladder Construction, November 2001","2001","10","16")
img8 = make_image(mock_flask_file_obj("test_images","FishLadderSmallSize.jpg"),"Fish Ladder Today","2009","6","6")

db.session.add(img1)
db.session.add(img2)
db.session.add(img3)
db.session.add(img4)
db.session.add(img5)
db.session.add(img6)
db.session.add(img7)
db.session.add(img8)

db.session.commit()

ip3_description = "Reed Lake was created sometime near the turn of the century by the construction of a 10-foot-high dam across Reed Creek. The creation of the dam blocked fish passage, as the creek was re-routed through a culvert system that discharged to a steep waterfall. \n \n Over the summer and fall of 2001, Reed College constructed a fish ladder to re-establish connectivity between Reed Lake and the lower creek for resident and anadromous fish."

ip1 = make_interest_point([img1.id,img2.id,img3.id],"Interest Point 1","This is a descriptions of something",geo_obj1,"Plants","Navy.png")
ip2 = make_interest_point([img4.id],"Interest Point 2","This is a descriptions of something else",geo_obj2,"Animals","Green.png")
ip3 = make_interest_point([img7.id,img8.id],"Fish Ladder",ip3_description,geo_obj3,"Interest Points","Green.png")


db.session.commit()
