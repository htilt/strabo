import os, os.path, re
from contextlib import closing

from PIL import Image

from strabo import app
from strabo import utils

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
  return utils.get_extension(filename) in app.config['ALLOWED_EXTENSIONS']

# This helper function uses PIL to make a new thumbnail of a given image
def make_thumbnail(image_filename,thumbnail_filename):
  # import desired image from /uploads folder
  img_fullpath = os.path.join(app.config['UPLOAD_FOLDER'],image_filename)
  img = Image.open(img_fullpath)
  # create a thumbnail from desired image
  # the thumbnail will have dimentions of the same ratio as before, capped by
  #the max dimention of max_size
  max_size = app.config["THUMBNAIL_MAX_SIZE"]
  img.thumbnail(max_size,Image.ANTIALIAS)
  # save the image under a new filename in thumbnails directory
  path = app.config['NEW_DATA_DIRECTORY']
  fullpath = os.path.join(path, thumbnail_filename)
  img.save(fullpath)

#get dimentions of item in uploads folder with the given filename
def get_dimentions(filename):
    with Image.open(os.path.join(app.config['UPLOAD_FOLDER'],filename)) as im:
        return im.size#width, height tuple
