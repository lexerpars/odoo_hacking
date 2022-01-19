# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 19:00:50 2022

@author: Usuario
"""
from . import auth
class Menu:
    
    def __init__(self,host):
        self.host = host
    
    
    def MenuOpciones(self):
        user = input('Ingrese un usuario de portal o interno valido >> ')
        password = input('Ingrese una clave valida para el usuario >> ')
        db = input('Espeficique la base de datos a auditar >> ')
        conexion = auth.Conexion(host=self.host)
        authentic = conexion.proxy('/xmlrpc/2/common')
        uid = authentic.authenticate(db,user,password,[])
        if not uid:
            print('Imposible continuar sin credenciales a la instancia!')
            return False
        op = True
        query = conexion.proxy('/xmlrpc/2/object')
        while op:
            
            print('[1] Obtener modelos de instancia')
            print('[x] Salir')
            
            opcion = input('>>')
            
            if opcion == '1':
                res = query.execute_kw(db,uid,password,'ir.model','search_read',[[]],{'fields':['name','model']})
                for r in res:
                    print(r)
                
            elif opcion == 'x':
                op = False
            else:
                print('Opcion no valida!')

                
    
    