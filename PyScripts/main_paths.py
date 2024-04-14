# -*- coding: utf-8 -*-
"""
@author: Alex Vu
"""

from os.path import join

# Namespace & Name
PACK_NAME = "SingleLoot"
PACK_NS = "single_loot"

# Data paths
DATA_ROOT = "..\\Data\\"
## Root for vanilla files that need to be changed with new data
DATA_TABLES_SRC_ROOT = join(DATA_ROOT, "BaseTables\\")
## Root for files that have been modified
DATA_TABLES_DST_ROOT = join(DATA_ROOT, "GeneratedTables\\")

# Datapack Base Path (for non-generated pack files)
PACK_SRC_ROOT = "..\\PackBase\\"

# Output Paths (for final datapack file)
PACK_DEPLOY_ROOT = "..\\{}\\".format(PACK_NAME)
## Functions
FUNCTIONS_SUBROOT = "data\\{}\\functions\\".format(PACK_NS)
FUNCTIONS_ROOT = join(PACK_DEPLOY_ROOT, FUNCTIONS_SUBROOT)
## Predicates
PREDICATES_SUBROOT = "data\\{}\\predicates\\".format(PACK_NS)
PREDICATES_ROOT = join(PACK_DEPLOY_ROOT, PREDICATES_SUBROOT)
## Recipes & Loot tables
TABLES_SUBROOT = "data\\minecraft\\"
TABLES_ROOT = join(PACK_DEPLOY_ROOT, TABLES_SUBROOT)
