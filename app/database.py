"""
database.py
------------------------------------------------------------
Módulo de acceso a datos para Las Golosinas del Firulais.
Usa SQLite (incluido en Python, no requiere instalar un
servidor de base de datos aparte).

Tablas:
  - Contacto  : mensajes del formulario de contacto
  - Categoria : categorías del catálogo (Tortas, Galletas, Kits)
  - Producto  : catálogo de productos
  - Oferta    : oferta(s) del mes, ligadas a un producto
  - Noticia   : noticias del emprendimiento (fecha, título, contenido, imagen)
------------------------------------------------------------
"""
import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "golosinas_firulais.db")


def obtener_conexion():
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


# ======================================================================
# CREACIÓN DE TABLAS
# ======================================================================
def crear_tablas():
    conexion = obtener_conexion()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS Contacto (
            id_contacto INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre      TEXT NOT NULL,
            email       TEXT NOT NULL,
            mensaje     TEXT NOT NULL,
            fecha       TEXT NOT NULL
        );
    """)

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS Categoria (
            id_categoria     INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_categoria TEXT NOT NULL,
            descripcion      TEXT
        );
    """)

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS Producto (
            id_producto     INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_producto TEXT NOT NULL,
            descripcion     TEXT,
            precio          REAL NOT NULL,
            stock           INTEGER DEFAULT 0,
            imagen          TEXT,
            id_categoria    INTEGER NOT NULL,
            FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria)
        );
    """)

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS Oferta (
            id_oferta     INTEGER PRIMARY KEY AUTOINCREMENT,
            id_producto   INTEGER NOT NULL,
            descripcion   TEXT NOT NULL,
            descuento     INTEGER NOT NULL,
            fecha_inicio  TEXT NOT NULL,
            fecha_fin     TEXT NOT NULL,
            activa        INTEGER DEFAULT 1,
            FOREIGN KEY (id_producto) REFERENCES Producto(id_producto)
        );
    """)

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS Noticia (
            id_noticia INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha      TEXT NOT NULL,
            titulo     TEXT NOT NULL,
            contenido  TEXT NOT NULL,
            imagen     TEXT
        );
    """)

    conexion.commit()
    conexion.close()


# ======================================================================
# DATOS INICIALES (SEED) — para que el sitio no aparezca vacío
# ======================================================================
def sembrar_datos_iniciales():
    conexion = obtener_conexion()

    ya_hay_categorias = conexion.execute("SELECT COUNT(*) AS n FROM Categoria").fetchone()["n"]
    if ya_hay_categorias == 0:
        categorias = [
            ("Tortas", "Tortas artesanales para perros y gatos"),
            ("Galletas", "Galletas horneadas sin azúcar ni chocolate"),
            ("Kits de fiesta", "Kits decorativos para celebraciones"),
        ]
        conexion.executemany(
            "INSERT INTO Categoria (nombre_categoria, descripcion) VALUES (?, ?)", categorias
        )
        conexion.commit()

    ya_hay_productos = conexion.execute("SELECT COUNT(*) AS n FROM Producto").fetchone()["n"]
    if ya_hay_productos == 0:
        productos = [
            ("Torta Mini Firulais", "Torta individual apta para razas pequeñas, decorada a mano.", 8.50, 20, "c6.png", 1),
            ("Torta Temática", "Torta personalizada según el tema de la fiesta (colores, nombre, edad).", 15.00, 15, "c7.png", 1),
            ("Kit Fiesta Grupal", "Torta grande + cupcakes individuales + gorros para hasta 6 mascotas.", 32.00, 8, "c9.png", 3),
            ("Galletas Artesanales (x12)", "Galletas horneadas sin azúcar ni chocolate, ideales para premiar a tu mascota.", 6.00, 30, "c4.png", 2),
            ("Combo Galletas + Torta Mini", "Perfecto para una celebración pequeña en casa.", 12.00, 10, "c1.png", 2),
            ("Kit Michi Especial", "Torta y snacks formulados especialmente para gatos.", 14.00, 12, "c3.png", 3),
        ]
        conexion.executemany(
            """INSERT INTO Producto (nombre_producto, descripcion, precio, stock, imagen, id_categoria)
               VALUES (?, ?, ?, ?, ?, ?)""",
            productos,
        )
        conexion.commit()

    ya_hay_ofertas = conexion.execute("SELECT COUNT(*) AS n FROM Oferta").fetchone()["n"]
    if ya_hay_ofertas == 0:
        id_kit_fiesta = conexion.execute(
            "SELECT id_producto FROM Producto WHERE nombre_producto = 'Kit Fiesta Grupal'"
        ).fetchone()["id_producto"]
        conexion.execute(
            """INSERT INTO Oferta (id_producto, descripcion, descuento, fecha_inicio, fecha_fin, activa)
               VALUES (?, ?, ?, ?, ?, 1)""",
            (id_kit_fiesta,
             "Celebramos el cumpleaños de la tienda regalando descuento en el Kit Fiesta Grupal: "
             "torta grande decorada, cupcakes individuales y gorros para hasta 6 mascotas.",
             30, "2026-08-01", "2026-08-31"),
        )
        conexion.commit()

    ya_hay_noticias = conexion.execute("SELECT COUNT(*) AS n FROM Noticia").fetchone()["n"]
    if ya_hay_noticias == 0:
        noticias = [
            ("2026-07-10", "¡Cumplimos 5 años consintiendo mascotas! 🎉",
             "Este mes celebramos 5 años como Las Golosinas del Firulais. Gracias a cada familia que "
             "confía en nosotros para las celebraciones de sus perros y gatos. Para agradecer, lanzamos "
             "la Oferta del Mes con 30% de descuento en nuestro Kit Fiesta Grupal.", "c1.png"),
            ("2026-07-02", "Nueva línea de galletas sin azúcar para gatos",
             "Ampliamos nuestro catálogo con galletas formuladas especialmente para gatos, sin azúcar "
             "ni ingredientes tóxicos para ellos. Ya disponibles en el catálogo de Productos.", "c6.png"),
            ("2026-06-20", "Ahora hacemos entregas a domicilio en todo Quito",
             "Para que no te compliques organizando la fiesta de tu mascota, ahora llevamos tu pedido "
             "hasta la puerta de tu casa. Coordina tu entrega escribiéndonos por WhatsApp.", "c9.png"),
        ]
        conexion.executemany(
            "INSERT INTO Noticia (fecha, titulo, contenido, imagen) VALUES (?, ?, ?, ?)", noticias
        )
        conexion.commit()

    conexion.close()


# ======================================================================
# CONTACTO
# ======================================================================
def guardar_contacto(nombre, email, mensaje):
    conexion = obtener_conexion()
    cursor = conexion.execute(
        "INSERT INTO Contacto (nombre, email, mensaje, fecha) VALUES (?, ?, ?, ?)",
        (nombre, email, mensaje, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    conexion.commit()
    nuevo_id = cursor.lastrowid
    conexion.close()
    return nuevo_id


def listar_contactos():
    conexion = obtener_conexion()
    filas = conexion.execute("SELECT * FROM Contacto ORDER BY id_contacto DESC").fetchall()
    conexion.close()
    return [dict(f) for f in filas]


def exportar_contactos_csv(ruta_csv):
    import csv
    contactos = listar_contactos()
    with open(ruta_csv, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["id_contacto", "nombre", "email", "mensaje", "fecha"])
        for c in contactos:
            escritor.writerow([c["id_contacto"], c["nombre"], c["email"], c["mensaje"], c["fecha"]])
    return ruta_csv


# ======================================================================
# PRODUCTOS (catálogo, para la opción Productos)
# ======================================================================
def listar_productos():
    conexion = obtener_conexion()
    filas = conexion.execute("""
        SELECT p.id_producto, p.nombre_producto, p.descripcion, p.precio, p.stock, p.imagen,
               c.nombre_categoria
        FROM Producto p
        INNER JOIN Categoria c ON p.id_categoria = c.id_categoria
        ORDER BY p.id_producto
    """).fetchall()
    conexion.close()
    return [dict(f) for f in filas]


# ======================================================================
# OFERTAS DEL MES
# ======================================================================
def listar_ofertas_activas():
    conexion = obtener_conexion()
    filas = conexion.execute("""
        SELECT o.id_oferta, o.descripcion, o.descuento, o.fecha_inicio, o.fecha_fin,
               p.id_producto, p.nombre_producto, p.precio, p.imagen
        FROM Oferta o
        INNER JOIN Producto p ON o.id_producto = p.id_producto
        WHERE o.activa = 1
        ORDER BY o.id_oferta DESC
    """).fetchall()
    conexion.close()
    return [dict(f) for f in filas]


# ======================================================================
# NOTICIAS
# ======================================================================
def listar_noticias():
    conexion = obtener_conexion()
    filas = conexion.execute("""
        SELECT id_noticia, fecha, titulo, contenido, imagen
        FROM Noticia
        ORDER BY fecha DESC
    """).fetchall()
    conexion.close()
    return [dict(f) for f in filas]
