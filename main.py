# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 21:03:02 2022

@author: Lexerpars
"""

import argparse
from models import auth

def parser():
    pars = argparse.ArgumentParser(description='Script hacking ODOO')
    pars.add_argument('host',help='URL o HOST de ODOO')
    arguments = pars.parse_args()
    return arguments

def main(arguments):
    welcome = '''
   ____      _                   _    _            _    _             
  / __ \    | |                 | |  | |          | |  (_)            
 | |  | | __| | ___   ___ ______| |__| | __ _  ___| | ___ _ __   __ _ 
 | |  | |/ _` |/ _ \ / _ \______|  __  |/ _` |/ __| |/ / | '_ \ / _` |
 | |__| | (_| | (_) | (_) |     | |  | | (_| | (__|   <| | | | | (_| |
  \____/ \__,_|\___/ \___/      |_|  |_|\__,_|\___|_|\_\_|_| |_|\__, |
  / ____|           | |                                          __/ |
 | |  __ _   _  __ _| |_ _____      ____ _ _ __ ___  ___        |___/ 
 | | |_ | | | |/ _` | __/ _ \ \ /\ / / _` | '__/ _ \/ __|             
 | |__| | |_| | (_| | ||  __/\ V  V / (_| | | |  __/\__ \             
  \_____|\__,_|\__,_|\__\___| \_/\_/ \__,_|_|  \___||___/             
                                                                      
                                                                                                                        
    '''
    print(welcome)
    print('[*] Target :',arguments.host)
    conexion = auth.Conexion(host=arguments.host)
    conexion.version()
    conexion.list_db()
    
    
if __name__ == '__main__':
    arguments = parser()
    main(arguments)

