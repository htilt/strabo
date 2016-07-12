""" 
This file contains utilities. 
"""

import os

def safe_pos_int_conv(inputstr):
    return  int(inputstr) if not inputstr == '' else 1

def extract_name_extention(filename):
    dot_loc = filename.rfind('.')

    find_not_found_value = -1
    dot_idx = dot_loc if dot_loc != find_not_found_value else len(filename) - 1

    return filename[:dot_idx], filename[dot_idx+1:]

def remove_extension(filename):
    return extract_name_extention(filename)[0]

def get_extension(filename):
    return extract_name_extention(filename)[1]
