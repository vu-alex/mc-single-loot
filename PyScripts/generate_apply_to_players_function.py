# -*- coding: utf-8 -*-

"""
@author: Alex Vu
"""

'''
Generate mcfunction and required files to apply the modifier to all
items inside all players' inventories.
'''

from main_paths import FUNCTIONS_ROOT, PREDICATES_ROOT, PACK_NS
from os import makedirs
from os.path import join

FUNCTION_NAME = "apply_to_players.mcfunction"

PREDICATE_PREFIX = "exception_slot_"
PREDICATE_RL = PACK_NS + ":{}"
ITEM_MODIFIER_RL = PACK_NS + ":set_single"

PREDICATE_CONTENT = [
    '{',
    '    "condition": "minecraft:entity_properties",',
    '    "entity": "this",',
    '    "predicate": {',
    '        "slots": {',
    '            "###": {',
    '                "items": "#single_loot:exceptions"',
    '            }',
    '        }',
    '    }',
    '}'
]

COMMAND_BASE = "execute as @a unless entity @s[predicate={}] run item modify entity @s {} {}"

SLOTS = [ ]

def generate_slots():
    global SLOTS
    SLOTS = []
    SLOTS += ["hotbar." + str(i) for i in range(9)]
    SLOTS += ["inventory." + str(i) for i in range(27)]
    SLOTS.append("player.cursor")
    SLOTS.append("weapon.offhand")

def generate_files():
    generate_slots()
    
    # Create missing directories for predicates) 
    makedirs(PREDICATES_ROOT, exist_ok=True)
    
    # Create missing directories for function, and open function file
    makedirs(FUNCTIONS_ROOT, exist_ok=True)
    function_path = join(FUNCTIONS_ROOT, FUNCTION_NAME)
    function_file = open(function_path, "w")
    
    for slot in SLOTS:
        # Compute names
        predicate_file_base = PREDICATE_PREFIX + slot.replace('.', '_')
        predicate = PREDICATE_RL.format(predicate_file_base)
        predicate_file_name = predicate_file_base + ".json"
        
        # Geneate command, and append it to function file
        command = COMMAND_BASE.format(predicate, slot, ITEM_MODIFIER_RL)
        function_file.write(command + "\n")
        
        # Generate predicate file
        predicate_path = join(PREDICATES_ROOT, predicate_file_name)
        predicate_file = open(predicate_path, "w")
        for line in PREDICATE_CONTENT:
            formatted_line = line.replace("###", slot)
            predicate_file.write(formatted_line + "\n")
        predicate_file.close()

    function_file.close()

def execute():
    generate_files()

if __name__ == '__main__':
    execute()

