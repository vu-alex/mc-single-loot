# -*- coding: utf-8 -*-
"""
@author: Alex Vu
"""

from main_paths import PACK_SRC_ROOT, PACK_DEPLOY_ROOT
from file_utils import copy_file_hierarchy, delete_dir_contents

def execute():
    # Clear deployment directory
    if (not delete_dir_contents(PACK_DEPLOY_ROOT)):
        return False
    
    # Copy base files
    copy_file_hierarchy(PACK_SRC_ROOT, PACK_DEPLOY_ROOT, '')
    return True

if __name__ == '__main__':
    execute()

