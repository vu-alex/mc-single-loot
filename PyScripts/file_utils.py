# -*- coding: utf-8 -*-
"""
@author: Alex Vu
"""

from os import listdir, makedirs, remove
from os.path import join, isdir, isfile, islink
from shutil import rmtree

def copy_file_hierarchy(src_dir: str, dst_dir: str, curr_sub_dir: str):
    src_dir_path = join(src_dir, curr_sub_dir)
    dst_dir_path = join(dst_dir, curr_sub_dir)
    
    for elem in listdir(src_dir_path):
        # Full path of element
        elem_full_path = join(src_dir_path, elem)
        # Path of element relative to source directory
        elem_sub_path = join(curr_sub_dir, elem)
        
        # Call recursively if directory
        if isdir(elem_full_path):
            copy_file_hierarchy(src_dir, dst_dir, elem_sub_path)
        # Else, open file/link and make a copy of its contents
        elif isfile(elem_full_path) or islink(elem_full_path):
            # Create missing directories for path
            makedirs(dst_dir_path, exist_ok=True)
            
            dst_elem_full_path = join(dst_dir_path, elem)
            
            # Copy source file to destination file with no edit
            src_file = open(elem_full_path, "r")
            dst_file = open(dst_elem_full_path, "w")
            
            data = src_file.read()
            dst_file.write(data)
            
            src_file.close()
            dst_file.close()
            
def delete_dir_contents(delete_root: str):
    if (not isdir(delete_root)):
        return True
    
    for elem in listdir(delete_root):
        try:
            # Full path of element
            elem_full_path = join(delete_root, elem)
            
            # Delete recursively if directory
            if isdir(elem_full_path):
                rmtree(elem_full_path)
            # Else, delete file/link
            elif isfile(elem_full_path) or islink(elem_full_path):
                remove(elem_full_path)
        except Exception as e:
            print('Could not delete "{}": {}'.format(elem_full_path, e))
            return False
    
    return True
        