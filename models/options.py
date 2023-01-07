# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 19:00:50 2022

@author: Usuario
"""
from . import auth
import time
import os
from . import default_models as dm
from getpass import getpass
directory = os.getcwd()
lista_modelos = []
class Menu:
    
    def __init__(self,host):
        self.host = host
        self.db = ''
        
    def check_access(self,uid,password,model,query):
        res={}
        for ac in ['read','write']:
            access = query.execute_kw(self.db,uid,password,model,'check_access_rights',[ac],{'raise_exception': False})
            res[ac] = access
        return res
    
    def fields_models(self,uid,password,model,query):
        fields = []
        field = query.execute_kw(self.db,uid,password,model,'fields_get',[],{})
        fields = [f for f in field]
        return fields
    
    def read_model(self,uid,password,model,query,fields):
        model = query.execute_kw(self.db,uid,password,model,'search_read',[],{'fields':fields})        
        if model:
            for m in model:
                print(m)
    
    def MenuOpciones(self,version):
        user = input('Ingrese un usuario de portal o interno valido >> ')
        password = getpass()
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
            print('[3] Fuerza bruta accesos a modelos')
            print('[4] Listar modelos disponibles')
            print('[5] Obtener informacion de modelo disponible')
            print('[x] Salir')
            
            opcion = input('>> ')
            
            if opcion == '1':
                acceso = self.check_access(uid, password, 'ir.model', query)
                print('Modelo : ir.model Access_Read : ',acceso['read'])
                print('Modelo : ir.model Access_write : ',acceso['write'])
                if acceso['read']:
                    res = query.execute_kw(self.db,uid,password,'ir.model','search_read',[[]],{'fields':['name','model']})
                    for r in res:
                        try:
                            print('*'*50)
                            a = self.check_access(uid, password, r['model'], query)
                            print('Model: ',r['model'])
                            print('Model name: ',r['name'])
                            print('Access: Read[',a['read'],']',' Write[',a['write'],']')
                            print('*'*50)
                            print('')
                            time.sleep(0.5)
                        except Exception as e:
                            pass
                        
                else:
                    pass
            if opcion == '2':
                acceso = self.check_access(uid, password, 'mail.mail', query)
                if acceso['read']:
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
                else:
                    print('No hay acceso a mail.mail')
            
            if opcion == '3':
                modelos = dm.default_models_odoo_old if version['version'] in ['9.0','10.0','11.0','12.0'] else dm.default_models_odoo_new
                verbose = input('Presione 1 para activar verbose!')
                lista_modelos =[]
                if not verbose:
                    print('Iniciando fuerza bruta!')
                for m in modelos:
                    try:
                        acceso = self.check_access(uid, password, m, query)
                        if verbose == '1':
                            print('*'*50)
                            print('Modelo : ',m,' Access_Read : [',acceso['read'],']')
                            print('Modelo : ',m,' Access_write : [',acceso['write'],']')
                            print('*'*50)
                            print('')
                        if acceso['read'] or acceso['write']:
                            lista_modelos.append(m)
                    except Exception as e:
                        pass
                print('Proceso finalizado!')
                    
            if opcion == '4':
                print('Listado de modelos disponibles')
                for m in lista_modelos:
                    print(str(lista_modelos.index(m)),' ',m)
            
            if opcion == '5':
                fields = self.fields_models(uid, password, 'res.partner', query)
                self.read_model(uid, password, 'res.users.log', query,['name'])
                
                        
            elif opcion == 'x':
                op = False

                
    
    
