import os, os.path
from contextlib import closing

from PIL import Image
from PIL.ExifTags import TAGS

from strabo import app

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This helper function uses PIL to make a new thumbnail of a given image
def make_thumbnail(filename, this_id):
  # import desired image from /uploads folder
  img = Image.open(app.config['UPLOAD_FOLDER'] + '/' + filename)
  # create a thumbnail from desired image
  size = 300, 300
  img.thumbnail(size)
  # save the image under a new filename in thumbnails directory
  imagename = filename.rsplit(".", 1)[0]
  newfilename = imagename + "_thumbnail.jpeg"
  path = app.config['NEW_DATA_DIRECTORY']
  fullpath = os.path.join(path, newfilename)
  img.save(fullpath)
  # return the filename for the thumbnail
  return newfilename

# Compatible with multiple phone types?
def DMS_to_Dec(lst):
  degrees = lst[0]
  minutes = lst[1]
  seconds = lst[2]
  dec = (seconds/3600) + (minutes/60) + degrees
  return(dec)

# This would be the desired implementation for server-side EXIF
# extraction. Currently, tags are extracted in javascript.
# def getEXIF(pathname, filename):
#   # Get path to file
#   total_pathname = os.path.join(pathname, filename)
#   # Extract EXIF data
#   date_created = Image.open(total_pathname)._getexif()[0x0132]
#   print(date_created)
#   return(date_created)