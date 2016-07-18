'''
Handles interaction with PIL library, including thumbnail creation, dimention getting, and
image processing capabilities, including allowed file extensions.
'''
import os
from PIL import Image

from strabo import utils

from strabo import app
from strabo import straboconfig

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return utils.get_extension(filename) in straboconfig['ALLOWED_EXTENSIONS']

# This helper function uses PIL to make a new thumbnail of a given image
def save_shrunken_image(image_path,thumbnail_path,max_dim):
    # import desired image from /uploads folder
    img = Image.open(image_path)
    # create a thumbnail from desired image
    # the thumbnail will have dimentions of the same ratio as before, capped by
    # the limiting dimention of max_dim
    img.thumbnail(max_dim,Image.ANTIALIAS)
    # save the image under a new filename in thumbnails directory
    img.save(thumbnail_path)

#get dimentions of item in uploads folder with the given filename
def get_dimentions(filename):
    with Image.open(os.path.join(straboconfig['UPLOAD_FOLDER'],filename)) as im:
        return im.size#width, height tuple
