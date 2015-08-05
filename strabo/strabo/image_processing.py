import os, os.path
from contextlib import closing

from PIL import Image

from strabo import app

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This helper function uses PIL to make a new thumbnail of a given image
def make_thumbnail(filename):
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