'''
Handles interaction with PIL library, including thumbnail creation, dimention getting, and
image processing capabilities, including allowed file extensions.
'''
import os
from PIL import Image

from strabo import utils

from strabo import app

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return utils.get_extension(filename) in app.config['ALLOWED_EXTENSIONS']

# This helper function uses PIL to make a new thumbnail of a given image
def save_as_thumbnail(image_path,thumbnail_path):
    # import desired image from /uploads folder
    img = Image.open(image_path)
    # create a thumbnail from desired image
    # the thumbnail will have dimentions of the same ratio as before, capped by
    # the max dimention of max_size
    max_size = app.config["THUMBNAIL_MAX_SIZE"]
    img.thumbnail(max_size,Image.ANTIALIAS)
    # save the image under a new filename in thumbnails directory
    img.save(thumbnail_path)

#get dimentions of item in uploads folder with the given filename
def get_dimentions(filename):
    with Image.open(os.path.join(app.config['UPLOAD_FOLDER'],filename)) as im:
        return im.size#width, height tuple
