'''
Overwrites thumbnails and mobile_imgs files with files of size specified in
configuration.

Use whenever the dimensions specified by THUMBNAIL_MAX_SIZE or MOBILE_SERV_MAX_SIZE
have been changed.
'''
import os

from strabo import file_writing
from strabo import image_processing

from strabo import straboconfig

for filename in os.listdir(os.path.join(straboconfig['STRABO_ABS_PATH'],"strabo/static/uploads/")):
    if image_processing.allowed_file(filename):
        file_writing.save_shrunken_images_with(filename)
