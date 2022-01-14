# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 21:10:44 2022

@author: Lexerpars
"""

from xmlrpc import client
from urllib import request
from bs4 import BeautifulSoup

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
    
    def registro_odoo(self):
        info_odoo = request.urlopen(self.host+'/web/login').read().decode()
        web = BeautifulSoup(info_odoo,'html.parser')
        etiquetas = web('a')
        signup = False
        reset_password = False
        for etiqueta in etiquetas:
            if 'web/signup' in etiqueta.get('href'):
                signup = True
                print('[*]Registro de usuario portal activo url :{}'.format(self.host+etiqueta.get('href')))
            if 'web/reset_password' in etiqueta.get('href'):
                reset_password = True
                print('[*]Permite retablecer la contraseña de usuarios url :{}'.format(self.host+etiqueta.get('href')))
        if not signup:
            print('[-]No posee registro de usuarios de portal')
        if not reset_password:
            print('[-]No permite restablecer las contraseñas')
                
                

        
    