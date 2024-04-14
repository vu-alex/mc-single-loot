# -*- coding: utf-8 -*-

"""
@author: Alex Vu
"""

import init_deployment
import create_tables
import deploy_tables
import generate_apply_to_players_function

if __name__ == '__main__':
    if (init_deployment.execute()):
        print('Deployment initialized.')
        create_tables.execute()
        print('Tables created.')
        deploy_tables.execute()
        print('Tables deployed.')
        generate_apply_to_players_function.execute()
        print('Apply to players function generated and deployed.')
