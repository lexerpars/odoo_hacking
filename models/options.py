# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 19:00:50 2022

@author: Usuario
"""
from . import auth
import time
import os
directory = os.getcwd()
class Menu:
    
    def __init__(self,host):
        self.host = host
        self.db = ''
    
    
    def MenuOpciones(self):
        user = input('Ingrese un usuario de portal o interno valido >> ')
        password = input('Ingrese una clave valida para el usuario >> ')
        self.db = input('Espeficique la base de datos a auditar >> ')
        conexion = auth.Conexion(host=self.host)
        authentic = conexion.proxy('/xmlrpc/2/common')
        uid = authentic.authenticate(self.db,user,password,[])
        if not uid:
            print('Imposible continuar sin credenciales a la instancia!')
            return False
        op = True
        query = conexion.proxy('/xmlrpc/2/object')
        while op:
            print('\n')
            print('[1] Obtener modelos de instancia')
            print('[2] Obtener mensajes')
            print('[x] Salir')
            
            opcion = input('>>')
            
            if opcion == '1':
                res = query.execute_kw(self.db,uid,password,'ir.model','search_read',[[]],{'fields':['name','model']})
                for r in res:
                    print(r)
            if opcion == '2':
                normaliza = lambda p : p if p else ''
                path = '\mails_'+self.db
                os.makedirs(directory+path, exist_ok=True)
                model_mail = query.execute_kw(self.db,uid,password,'mail.mail','search_read',[[]],{'fields':['name']})
                print(model_mail)
                print(len(model_mail), 'Registros encontrados!')
                print('Procesando informacion!')
                for record in model_mail:
                    record_mail = query.execute_kw(self.db,uid,password,'mail.mail','search_read',[[['id','=',record['id']]]],{'fields':['body_html','email_to','email_from']})
                    if record_mail:
                        record_mail =record_mail[0]
                        with open('./mails_{}/'.format(self.db)+str(record['id'])+'.html','w') as f:
                            f.write('email_to '+normaliza(record_mail['email_to']))
                            f.write('email_from '+normaliza(record_mail['email_from']))
                            f.write(record_mail['body_html'])
                            f.close()
                    time.sleep(4)
                        
                
            elif opcion == 'x':
                op = False
            else:
                print('Opcion no valida!')

                
    
    