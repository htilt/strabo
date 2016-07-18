'''
This file deals with image file naming, paths, and saving and deleting.
'''
import werkzeug
import os
import random

from strabo import image_processing
from strabo import utils

from strabo import app
from strabo import straboconfig

def get_image_path(filename):
    return os.path.join(straboconfig['UPLOAD_FOLDER'], filename)

def get_mobile_img_path(filename):
    return os.path.join(straboconfig['MOBILE_IMG_DIR'], filename)

def get_thumbnail_path(filename):
    return os.path.join(straboconfig['THUMB_DIR'], filename)

#generates a filename which does not yet iexist in the folder specified by path
def make_unique_filename(path,filename):
    def gen_new_name():
        name,ext = utils.extract_name_extention(filename)
        return name+str(random.randint(0,1000000000000000)) + '.' + ext

    uniq_name = filename
    while os.path.isfile(os.path.join(path,uniq_name)):
        uniq_name = gen_new_name()

    return uniq_name

#gives a safe filename that is not the same as any other in the uploads folder
def make_filename(form_file_name):
    secure_filename = werkzeug.secure_filename(form_file_name)
    # prepend unique id to ensure an unique filename
    unique_filename = make_unique_filename(straboconfig['UPLOAD_FOLDER'],secure_filename)
    return  unique_filename


def save_shrunken_images_with(filename):
    '''Make a thumbnail and mobile_imgs and store it in the appropriate directory
    using the same filename as the original image. '''
    image_processing.save_shrunken_image(get_image_path(filename),get_thumbnail_path(filename),straboconfig["THUMBNAIL_MAX_SIZE"])
    #do the same with different dimentions to mobile_imgs
    image_processing.save_shrunken_image(get_image_path(filename),get_mobile_img_path(filename),straboconfig["MOBILE_SERV_MAX_SIZE"])


#saves image and thumbnail using the given filenaem
def save_image_files(form_file_obj,filename):
    #if no files is attached, then do nothing
    if not form_file_obj:
        return
    #if the file extension is not allowed,throw an error
    #todo: put this error in the frontend instead of here
    if not image_processing.allowed_file(form_file_obj.filename):
        raise RuntimeError("file extension not allowed")

    # Move the file from the temporary folder to the upload folder
    form_file_obj.save(get_image_path(filename))
    #note that unique filename in uploads folder will also be unique filename in other folders
    save_shrunken_images_with(filename)

#delete image helper functions
def delete_image_files(filename):
    os.remove(get_image_path(filename))
    os.remove(get_thumbnail_path(filename))
    os.remove(get_mobile_img_path(filename))
