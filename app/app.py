"""
app.py
------------------------------------------------------------
Aplicación Flask de Las Golosinas del Firulais.

Sirve el sitio web (HTML/CSS/JS/jQuery) y expone dos rutas de API:

  POST /api/contacto   -> guarda un mensaje del formulario de Contacto
                           en la tabla Contacto (SQLite) y responde con
                           un mensaje de confirmación (acuse de recibido).

  GET  /api/clima       -> consulta el clima actual (OpenWeatherMap)
                           y devuelve temperatura, humedad, descripción
                           y viento.
------------------------------------------------------------
"""
import os
import re
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

import database
import weather

load_dotenv()  # Carga variables desde el archivo .env (por ejemplo, el API Key del clima)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web")

app = Flask(__name__, static_folder=WEB_DIR, static_url_path="")
database.crear_tablas()
database.sembrar_datos_iniciales()

REGEX_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# ------------------------------------------------------------------
# Servir el sitio web estático (Home, Empresa, Productos, etc.)
# ------------------------------------------------------------------
@app.route("/")
def home():
    return send_from_directory(WEB_DIR, "index.html")


@app.route("/<path:nombre_archivo>")
def archivos_estaticos(nombre_archivo):
    return send_from_directory(WEB_DIR, nombre_archivo)


# ------------------------------------------------------------------
# API: Contacto -> guarda en la base de datos (Create)
# ------------------------------------------------------------------
@app.route("/api/contacto", methods=["POST"])
def api_contacto():
    datos = request.get_json(silent=True) or {}
    nombre = (datos.get("nombre") or "").strip()
    email = (datos.get("email") or "").strip()
    mensaje = (datos.get("mensaje") or "").strip()

    errores = {}
    if not nombre:
        errores["nombre"] = "El nombre es obligatorio."
    if not email or not REGEX_EMAIL.match(email):
        errores["email"] = "Ingresa un correo electrónico válido."
    if not mensaje:
        errores["mensaje"] = "El mensaje es obligatorio."

    if errores:
        return jsonify({"ok": False, "errores": errores}), 400

    id_contacto = database.guardar_contacto(nombre, email, mensaje)

    # "Acuse de recibido": mensaje de confirmación que ve el usuario
    # apenas se guarda su registro en la base de datos.
    return jsonify({
        "ok": True,
        "id_contacto": id_contacto,
        "mensaje": f"¡Gracias, {nombre}! Hemos recibido tu mensaje correctamente "
                   f"(código de referencia #{id_contacto}). Te contactaremos pronto.",
    })


# ------------------------------------------------------------------
# API: Clima -> consulta OpenWeatherMap (Read desde un servicio externo)
# ------------------------------------------------------------------
@app.route("/api/clima", methods=["GET"])
def api_clima():
    ciudad = request.args.get("ciudad", "Quito,EC")
    resultado = weather.obtener_clima(ciudad)
    if not resultado.get("ok"):
        return jsonify(resultado), 502
    return jsonify(resultado)


# ------------------------------------------------------------------
# API: Productos -> catálogo completo (Read desde la base de datos)
# ------------------------------------------------------------------
@app.route("/api/productos", methods=["GET"])
def api_productos():
    return jsonify(database.listar_productos())


# ------------------------------------------------------------------
# API: Ofertas del mes -> ofertas activas (Read desde la base de datos)
# ------------------------------------------------------------------
@app.route("/api/ofertas", methods=["GET"])
def api_ofertas():
    return jsonify(database.listar_ofertas_activas())


# ------------------------------------------------------------------
# API: Noticias -> tabla Noticia (Read desde la base de datos)
# ------------------------------------------------------------------
@app.route("/api/noticias", methods=["GET"])
def api_noticias():
    return jsonify(database.listar_noticias())



