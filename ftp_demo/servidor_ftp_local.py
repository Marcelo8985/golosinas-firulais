"""
servidor_ftp_local.py
------------------------------------------------------------
Servidor FTP LOCAL de pruebas, construido con la librería
pyftpdlib. Se usa únicamente para poder demostrar la subida de
archivos por FTP en la actividad académica, ya que el
emprendimiento no cuenta con un servidor FTP propio contratado.

Cómo se usa:
  1. Ejecutar este script en una terminal:  python servidor_ftp_local.py
  2. Dejarlo corriendo (queda "escuchando" en 127.0.0.1:2121)
  3. En OTRA terminal, ejecutar subir_ftp.py para subir un archivo

Usuario: firulais
Contraseña: golosinas123
Carpeta raíz del FTP: ./ftp_storage
------------------------------------------------------------
"""
import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

CARPETA_FTP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ftp_storage")
os.makedirs(CARPETA_FTP, exist_ok=True)

USUARIO = "firulais"
CLAVE = "golosinas123"
HOST = "127.0.0.1"
PUERTO = 2121


def iniciar_servidor():
    autorizador = DummyAuthorizer()
    # Permisos: e=entrar, l=listar, r=leer, a=agregar/subir, d=borrar, m=crear carpeta, w=escribir
    autorizador.add_user(USUARIO, CLAVE, CARPETA_FTP, perm="elradfmw")

    manejador = FTPHandler
    manejador.authorizer = autorizador
    manejador.banner = "Servidor FTP local - Las Golosinas del Firulais"

    servidor = FTPServer((HOST, PUERTO), manejador)
    print(f"Servidor FTP local escuchando en ftp://{HOST}:{PUERTO}")
    print(f"Usuario: {USUARIO}  |  Carpeta raíz: {CARPETA_FTP}")
    servidor.serve_forever()


if __name__ == "__main__":
    iniciar_servidor()
