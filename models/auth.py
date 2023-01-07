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
            try:
                version = res['server_serie']
                tipo = 'Enterprise' if 'e' in res['server_version_info'][5].lower() else 'Community'
                protocolo = res['protocol_version']
                print('Version ODOO: ',version)
                print('Tipo: ',tipo)
                print('Version protocolo: ',protocolo)
                return {'version':version,'tipo':tipo,'protocolo':protocolo}
            except Exception as e:
                print('Este servidor no soporta el metodo version')
                return False
    
    def list_db(self):
        try:
            conn = self.proxy('/xmlrpc/db')
            db = conn.list()
            print('[*] Listado de bases de datos: ',db)
            return db
        except Exception as e:
            if 'Access denied' in str(e):
                print('Acceso denegado: No se pueden listar las bases de datos')
            else:
                print('Ocurrio un problema: ',str(e))
    
    def registro_odoo(self):
        try:
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
        except Exception as e:
            print('/web/login [{}]'.format(e))
    
    def apps_default_info(self):
        try:
            website_info = request.urlopen(self.host+'/website/info').read().decode()
            website = BeautifulSoup(website_info,'html.parser')
            etiquetas = website.select('dt a')
            modulos = []
            print('[*] Website info')
            print('Aplicaciones instaladas')
            for etiqueta in etiquetas:
                modulos.append([etiqueta.text.replace('\n','').replace(' ',''), etiqueta.get('href').replace('\n','').replace(' ','')])
            for modulo in modulos:
                print(modulo)
            return modulos
                
        except Exception as e:
            print(self.host+'/website/info ',str(e))
    
    def auth_basic(self,dbs):
        users = ['admin','administrador','administrator']
        passwords = ['admin','123','1234','12345','123456']
        auth = self.proxy('/xmlrpc/2/common')
        result = []
        for db in dbs:
            print('[*] Probando usuarios y claves para base de datos: ',db)
            for user in users:
                for password in passwords:
                    uid = auth.authenticate(db,user,password,[])
                    if uid:
                        print('CREDENDECIALES VALIDAS usuario: ',user,' contraseña: ',password, ' DB: ',db)
                        result.append([user,password,db])
                        break
        if result:
            print('[*] Credenciales validas: ',result)
        if not result:
            print('[-] Credenciales default probadas - ninguna es valida')
        return result
                    
        
                
                

        
    
