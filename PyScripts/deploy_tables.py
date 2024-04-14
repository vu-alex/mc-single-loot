# -*- coding: utf-8 -*-
"""
@author: Alex Vu
"""

'''
Copies the generated loot tables & recipe files 
to the datapack folder
'''

from main_paths import DATA_TABLES_DST_ROOT, TABLES_ROOT
from file_utils import copy_file_hierarchy

def execute():
    copy_file_hierarchy(DATA_TABLES_DST_ROOT, TABLES_ROOT, '')

if __name__ == '__main__':
    execute()
