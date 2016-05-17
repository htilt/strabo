from strabo import schema_livy
from strabo import database
from strabo.utils import make_date

# This function loads in the proper sql table if it doesn't already exist.
def intiate_db():
    schema_livy.Base.metadata.create_all(database.engine)

if __name__ == '__main__':
  #intiate_db()
  database.insert_images({
    "title":"mytitle",
    "img_description":"this is an image",
    "latitude":3.4,
    "longitude":3.52,
    "date_created":make_date(10, 5, 1992),
    "interest_point":"",
    "event":"",
    "period":"",
    "notes":"",
    "tags":"",
    "edited_by":"ben",
    "filename":"fakefilename",
    "thumbnail_name":"fakegthumbnailname"})
    
  database.insert_images({
      "title":"mytitle",
      "img_description":"this is an image",
      "latitude":3.4,
      "longitude":3.52,
      "date_created":make_date(10, 5, 1992),
      "interest_point":"",
      "event":"",
      "period":"",
      "notes":"",
      "tags":"",
      "edited_by":"ben",
      "filename":"fakefilename",
      "thumbnail_name":"fakegthumbnailname"})
'''
(title, img_description, latitude, longitude,
  date_created, interest_point, event, period, notes, tags,
  edited_by, filename, thumbnail_name)
'''
