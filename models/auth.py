# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 21:10:44 2022

@author: Lexerpars
"""

from xmlrpc import client

class Conexion:
    
    def __init__(self,host):
        self.host = host
    
    def proxy(self,resource):
        conexion = client.ServerProxy('{}{}'.format(self.host,resource))
        return conexion
    
    
    def version(self):
        conn = self.proxy('/xmlrpc/2/common')
        res = conn.version()
        if res:
            version = res['server_serie']
            tipo = 'Enterprise' if 'e' in res['server_version_info'][5].lower() else 'Community'
            protocolo = res['protocol_version']
            print('Version ODOO: ',version)
            print('Tipo: ',tipo)
            print('Version protocolo: ',protocolo)
            return {'version':version,'tipo':tipo,'protocolo':protocolo}
        else:
            print('Este servidor no soporta el metodo version')
            return False
    
    def list_db(self):
        try:
            conn = self.proxy('/xmlrpc/db')
            db = conn.list()
            print(db)
            return db
        except Exception as e:
            if 'Access denied' in str(e):
                print('Acceso denegado: No se pueden listar las bases de datos')
            else:
                print('Ocurrio un problema: ',str(e))

        
    