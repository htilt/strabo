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

def make_unique_filename(path,filename):
    '''generates a filename with the given properties

    #. The new filename does not exist yet in the folder specified by ``path``.
    #. The filename has the same file extension as the ``filename`` argument.

    Note that the uniqueness is only gaurenteed if the app is run in a single thread/process
    , but it really ought to be fine in any case.
    '''
    def gen_new_name():
        name,ext = utils.extract_name_extension(filename)
        return name+str(random.randint(0,1000000000000000)) + '.' + ext

    uniq_name = filename
    while os.path.isfile(os.path.join(path,uniq_name)):
        uniq_name = gen_new_name()

    return uniq_name

def make_filename(form_file_name):
    '''
    uses make_unique_filename to make a safe filename that is not the same as any other in the uploads folder
    '''
    secure_filename = werkzeug.secure_filename(form_file_name)
    # prepend unique id to ensure an unique filename
    unique_filename = make_unique_filename(straboconfig['UPLOAD_FOLDER'],secure_filename)
    return  unique_filename


def save_shrunken_images_with(filename):
    '''
    Assumes that ``filename`` is a image file already stored in the uploads directory.

    Generates a thumbnail and mobile_img and saves them under ``filename``
    in their appropriate directory.
    '''
    image_processing.save_shrunken_image(get_image_path(filename),get_thumbnail_path(filename),straboconfig["THUMBNAIL_MAX_SIZE"])
    #do the same with different dimentions to mobile_imgs
    image_processing.save_shrunken_image(get_image_path(filename),get_mobile_img_path(filename),straboconfig["MOBILE_SERV_MAX_SIZE"])


#saves image and thumbnail using the given filenaem
def save_image_files(form_file_obj,filename):
    '''
    Checks saves ``form_file_obj``
    under ``uploads/<filename>``.

    Throws an error if form_file_obj is of not an allowed file extension.
    Ideally, this possibility would be not be allowed through form validation.
    '''
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

def safe_file_remove(filepath):
    '''If the file exists, then delete it, else do nothing.'''
    if os.path.isfile(filepath):
        os.remove(filepath)
        
def delete_image_files(filename):
    '''
    Deletes uploaded image and all images generated from it.
    '''
    safe_file_remove(get_image_path(filename))
    safe_file_remove(get_thumbnail_path(filename))
    safe_file_remove(get_mobile_img_path(filename))
