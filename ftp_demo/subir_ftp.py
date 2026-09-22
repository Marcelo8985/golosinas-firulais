"""
subir_ftp.py
------------------------------------------------------------
Script solicitado en el Paso 1, punto 5: "Subir a FTP mediante
el módulo ftplib de Python".

Este script:
  1. Exporta la tabla Contacto (SQLite) a un archivo .csv
  2. Se conecta al servidor FTP usando ftplib
  3. Sube (STOR) ese archivo .csv al servidor FTP

Por defecto apunta al servidor FTP LOCAL de pruebas
(servidor_ftp_local.py). Si el negocio contrata un hosting con
FTP real, solo hay que cambiar HOST, USUARIO, CLAVE y PUERTO
por los datos que entregue el proveedor de hosting.
------------------------------------------------------------
"""
import os
import sys
from ftplib import FTP

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "app"))
import database  # noqa: E402  (módulo del backend Flask, tabla Contacto)

# ------------------ Configuración del servidor FTP ------------------
HOST = "127.0.0.1"
PUERTO = 2121
USUARIO = "firulais"
CLAVE = "golosinas123"
# ----------------------------------------------------------------------


def generar_csv_contactos():
    ruta_local = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contactos_export.csv")
    database.exportar_contactos_csv(ruta_local)
    print(f"Archivo generado: {ruta_local}")
    return ruta_local


def subir_archivo_ftp(ruta_archivo):
    nombre_archivo = os.path.basename(ruta_archivo)

    ftp = FTP()
    ftp.connect(HOST, PUERTO, timeout=10)
    ftp.login(USUARIO, CLAVE)
    print("Conectado al servidor FTP:", ftp.getwelcome())

    with open(ruta_archivo, "rb") as archivo:
        ftp.storbinary(f"STOR {nombre_archivo}", archivo)

    print(f"Archivo '{nombre_archivo}' subido correctamente por FTP.")
    print("Contenido actual del servidor FTP:", ftp.nlst())

    ftp.quit()


if __name__ == "__main__":
    ruta_csv = generar_csv_contactos()
    subir_archivo_ftp(ruta_csv)
