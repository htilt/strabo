import os, os.path, re
from contextlib import closing

from PIL import Image

from strabo import app
from strabo import utils

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
  return utils.get_extension(filename) in app.config['ALLOWED_EXTENSIONS']

# This helper function uses PIL to make a new thumbnail of a given image
def make_thumbnail(filename):
  # import desired image from /uploads folder
  img_fullpath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
  img = Image.open(img_fullpath)
  # create a thumbnail from desired image
  size = 300, 300
  img.thumbnail(size)
  # save the image under a new filename in thumbnails directory
  path = app.config['NEW_DATA_DIRECTORY']
  fullpath = os.path.join(path, filename)
  img.save(fullpath)
