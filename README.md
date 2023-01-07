# odoo_hacking
Herramienta de hacking para Odoo

Realiza una auditoria inicial de manera automatica.
Obtiene la siguiente informacion:
- Version de Odoo
- Tipo
- Version de protocolo
- Listado de bases de datos
- Verificacion de registro de usuarios de portal
- Verificacion de opcion restablecer contraseña
- Prueba rapida de fuerza bruta de usuarios y claves

Uso: python main.py url
Ejemplo url = https://www.guatewares.com , http://localhost, http://192.0.0.1
python main.py http://localhost:8069
python3 main.py http://localhost:8069

Requiere BS4 para su funcionamiento:
sudo apt-get install python3-bs4
