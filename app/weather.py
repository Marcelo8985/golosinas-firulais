"""
weather.py
------------------------------------------------------------
Módulo que consulta el clima actual usando la API gratuita
de OpenWeatherMap (https://openweathermap.org/api).

Para que funcione con datos reales, hay que:
  1. Crear una cuenta gratuita en https://openweathermap.org/
  2. Generar un API Key en https://home.openweathermap.org/api_keys
  3. Pegar ese API Key en el archivo .env (variable OPENWEATHER_API_KEY)

Mientras no exista una API Key válida, la función devuelve un
error controlado para que el resto de la aplicación no se caiga.
------------------------------------------------------------
"""
import os
import requests

URL_BASE = "https://api.openweathermap.org/data/2.5/weather"


def obtener_clima(ciudad="Quito,EC"):
    """
    Consulta el clima actual de una ciudad.
    Devuelve un diccionario con: temperatura, humedad, descripcion, viento.
    """
    api_key = os.environ.get("OPENWEATHER_API_KEY", "")

    if not api_key:
        return {
            "ok": False,
            "error": "No se ha configurado OPENWEATHER_API_KEY. "
                     "Crea tu cuenta y tu API Key en openweathermap.org y "
                     "colócala en el archivo .env",
        }

    parametros = {
        "q": ciudad,
        "appid": api_key,
        "units": "metric",     # grados Celsius
        "lang": "es",          # descripción en español
    }

    try:
        respuesta = requests.get(URL_BASE, params=parametros, timeout=8)
        datos = respuesta.json()

        if respuesta.status_code != 200:
            return {"ok": False, "error": datos.get("message", "Error consultando el clima")}

        return {
            "ok": True,
            "ciudad": datos.get("name", ciudad),
            "temperatura": round(datos["main"]["temp"], 1),
            "sensacion_termica": round(datos["main"]["feels_like"], 1),
            "humedad": datos["main"]["humidity"],
            "descripcion": datos["weather"][0]["description"].capitalize(),
            "viento": datos["wind"]["speed"],
        }

    except requests.exceptions.RequestException as error:
        return {"ok": False, "error": f"No se pudo conectar con OpenWeatherMap: {error}"}
