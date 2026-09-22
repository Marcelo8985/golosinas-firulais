# Cómo ejecutar el proyecto en tu computador

## 1) Verifica que tengas Python instalado
Abre una terminal (CMD o PowerShell en Windows) y escribe:
    python --version
Si te sale un número de versión (por ejemplo Python 3.12), continúa al paso 2.
Si te dice que no reconoce el comando, descarga Python desde https://www.python.org/downloads/
(al instalar, marca la casilla "Add Python to PATH").

## 2) Instala las dependencias
Abre una terminal DENTRO de la carpeta "app" y ejecuta:
    pip install -r ../requirements.txt

## 3) Ejecuta el servidor
Todavía dentro de la carpeta "app":
    python app.py

Debe aparecer un mensaje como "Running on http://127.0.0.1:5000". Déjalo corriendo.

## 4) Abre el sitio en tu navegador
Ve a: http://127.0.0.1:5000/clima.html
Dale clic al botón "Ver clima actual" y toma una captura de pantalla del resultado.

## 5) Prueba también el formulario de Contacto (opcional, ya lo probé yo, pero puedes verlo tú también)
Ve a: http://127.0.0.1:5000/contacto.html
Llena el formulario y dale clic en "Guardar".

## 6) Para detener el servidor
Vuelve a la terminal y presiona CTRL + C
