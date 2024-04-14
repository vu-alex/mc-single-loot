# -*- coding: utf-8 -*-
"""
@author: Alex Vu
"""

'''
Apply the "single-item" and "unstackable" modifier 
to loot tables and recipes inside the source folder (SRC_ROOT), 
and outputs the results into the destination folder (DST_ROOT)
'''

from main_paths import DATA_TABLES_SRC_ROOT, DATA_TABLES_DST_ROOT

import json
from os import listdir, makedirs
from os.path import isfile, join

CRAFTING_TYPES = [
    'minecraft:crafting_shaped',
    'minecraft:crafting_shapeless',
    'minecraft:stonecutting',
    'minecraft:smelting',
    'minecraft:smoking',
    'minecraft:blasting',
    'minecraft:campfire_cooking',
    'minecraft:smithing_transform'
]

def edit_files(src_dir: str, dst_dir: str, curr_sub_dir: str):
    src_dir_path = join(src_dir, curr_sub_dir)
    dst_dir_path = join(dst_dir, curr_sub_dir)
    
    for elem in listdir(src_dir_path):
        # Full path of element
        elem_full_path = join(src_dir_path, elem)
        # Path of element relative to source directory
        elem_sub_path = join(curr_sub_dir, elem)
        
        # Call recursively if directory
        if not isfile(elem_full_path):
            edit_files(src_dir, dst_dir, elem_sub_path)
        # Else, open file and make a copy of it
        else:
            # Create missing directories for path
            makedirs(dst_dir_path, exist_ok=True)
            
            dst_elem_full_path = join(dst_dir_path, elem)
            
            # Open files (source (read) and destination (write))
            src_file = open(elem_full_path, "r")
            dst_file = open(dst_elem_full_path, "w")
            
            # Read and parse file data
            src_data_str = src_file.read()
            data_obj = json.loads(src_data_str)
            
            # Edit object, and write to file
            if ('loot_tables' in elem_sub_path):
                # print(elem_sub_path)
                pass
                
            edit_object(data_obj, data_obj)
            dst_data_str = json.dumps(data_obj, indent=2)
            dst_file.write(dst_data_str)
            
            # Close files
            src_file.close()
            dst_file.close()

def edit_item(obj: dict, root: dict):
    # Add "functions" field if not available
    if ('functions' not in obj):
        obj['functions'] = []
    
    # Check for existing functions
    components_index = -1
    looting_index = -1
    fortune_index = -1
    loop_index = -1
    is_for_entity = root['type'] == 'minecraft:entity'
    
    for elem in obj['functions']:
        loop_index += 1
        
        if (elem['function'] == 'minecraft:set_components'):
            components_index = loop_index
        elif (elem['function'] == 'minecraft:set_count'):
            count = elem['count']
            if isinstance(count, dict):
                if (count['type'] == 'minecraft:uniform'):
                    if (is_for_entity):
                        pass
                    else:
                        count['max'] = min(count['max'], 1.0)
                        count['min'] = min(count['min'], 1.0)
                else:
                    pass
            elif isinstance(count, float):
                elem['count'] = min(count, 1.0)
            else:
                print(count)
        
        elif (elem['function'] == 'minecraft:looting_enchant'):
            looting_index = loop_index
        elif (elem['function'] == 'minecraft:apply_bonus'):
            fortune_index = loop_index
    
    # Add components' function if it does not exist
    if (components_index == -1):
        components_index = len(obj['functions'])
        obj['functions'].append({
            'components': {},
            'function': 'minecraft:set_components'
        })
    
    # Apply max stack size component
    components = obj['functions'][components_index]['components']
    components['max_stack_size'] = 1
    
    # Nerf multi-drop
    if (fortune_index != -1):
        #if (obj['name'] == 'minecraft:wheat_seeds') or (obj['name'] == 'minecraft:beetroot_seeds'):
        if (obj['functions'][fortune_index]['formula'] == 'minecraft:binomial_with_bonus_count'):
            del obj['functions'][fortune_index]
        elif (obj['functions'][fortune_index]['formula'] == 'minecraft:uniform_bonus_count'):
            del obj['functions'][fortune_index]
        elif (obj['functions'][fortune_index]['formula'] == 'minecraft:ore_drops'):
            del obj['functions'][fortune_index]
        else:
            print(obj)
    elif (looting_index != -1):
        del obj['functions'][looting_index]
        
    # Limit entity drops (different way because of smelting modifier)
    if (is_for_entity):
        # Search for a "set_count" function
        loop_index = -1
        for elem in obj['functions']:
            loop_index += 1
            set_count_index = -1
            if (elem['function'] == 'minecraft:set_count'):
                set_count_index = loop_index
                break
        # If "set_count" function exists, limit the count right after it
        if (set_count_index != -1):
            # Create a function to limit the count to at most 1
            limit_function = {
                "limit": {
                    "max": 1,
                    "min": 0
                },
                "function": "minecraft:limit_count"
            }
            # Insert function
            obj['functions'].insert(set_count_index + 1, limit_function)
        

def edit_crafting(obj: dict, root: dict):
    if ('result' not in obj):
        print(obj)
        return
    
    result = obj['result']
    if ('components' not in result):
        result['components'] = {}
    
    # Set result's count to 1
    if ('count' in result):
        result['count'] = 1
    
    # Apply max stack size component
    components = result['components']
    components['max_stack_size'] = 1

def edit_object(obj: dict, root: dict):
    if ('type' in obj):
        if (obj['type'] == 'minecraft:item'):
            edit_item(obj, root)
            return
        elif (obj['type'] in CRAFTING_TYPES):
            edit_crafting(obj, root)
            return
        elif ('result' in obj):
            # print(obj['type'])
            pass
        else:
            # print(obj['type'])
            pass

    for name in obj:
        value = obj[name]
        edit_value(value, root)
        
def edit_value(value: any, root: dict):
    if isinstance(value, dict):
        edit_object(value, root)
    elif (isinstance(value, list)):
        for elem in value:
            edit_value(elem, root)
    else:
        pass

def execute():
    edit_files(DATA_TABLES_SRC_ROOT, DATA_TABLES_DST_ROOT, '')

if __name__ == '__main__':
    execute()

