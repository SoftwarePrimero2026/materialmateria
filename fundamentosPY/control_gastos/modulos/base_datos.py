"""Acceso a SQLite con la biblioteca nativa `sqlite3` (sin ORM).

Este módulo es la única capa que habla con la base de datos: abre la
conexión, crea las tablas y ejecuta las consultas. El resto de la app
no necesita saber nada de SQLite.

TODAS las sentencias SQL viven en `gastos.sql` (al lado de este archivo)
y se cargan acá:
  - ZONA 1 (esquema): se ejecuta con `executescript()` al conectar.
  - ZONA 2 (consultas): se parsean en el diccionario `CONSULTAS`, cada
    una identificada por su nombre (`-- @nombre`).

Para cambiar o agregar una sentencia, se edita únicamente `gastos.sql`.
"""

import sqlite3
from pathlib import Path

# ---------------------------------------------------------------- rutas
# La base de datos y el archivo de SQL viven en la raíz de la carpeta
# `control_gastos/`, es decir, un nivel más arriba que `modulos/`.
RUTA_DB = Path(__file__).resolve().parent.parent / "gastos.db"
RUTA_SQL = Path(__file__).resolve().parent.parent / "gastos.sql"

# --------------------------------------------------- marcadores SQL
# Los marcadores delimitan las dos zonas dentro de `gastos.sql`.
MARCA_INICIO_ESQUEMA = "-- ===INICIO ESQUEMA==="
MARCA_FIN_ESQUEMA = "-- ===FIN ESQUEMA==="
MARCA_INICIO_CONSULTAS = "-- ===INICIO CONSULTAS==="
MARCA_FIN_CONSULTAS = "-- ===FIN CONSULTAS==="


def _leer_bloque(marca_inicio, marca_fin):
    """Devuelve el texto que está entre dos marcadores de `gastos.sql`."""
    texto = RUTA_SQL.read_text(encoding="utf-8")
    inicio = texto.index(marca_inicio) + len(marca_inicio)
    fin = texto.index(marca_fin)
    return texto[inicio:fin]


def _leer_esquema():
    """Devuelve las sentencias de la ZONA 1 (CREATE TABLE e INSERT)."""
    return _leer_bloque(MARCA_INICIO_ESQUEMA, MARCA_FIN_ESQUEMA)


def _leer_consultas():
    """Parsea la ZONA 2 de `gastos.sql` y devuelve {nombre: sentencia}.

    Cada consulta está marcada con un comentario `-- @nombre` y termina
    con ";". Las líneas de comentario y las vacías se ignoran.
    """
    consultas = {}
    nombre = None
    sentencia = []

    for linea in _leer_bloque(MARCA_INICIO_CONSULTAS, MARCA_FIN_CONSULTAS).splitlines():
        limpia = linea.strip()
        if limpia.startswith("-- @"):
            if nombre is not None:
                consultas[nombre] = " ".join(sentencia).strip()
            nombre = limpia[4:].strip()
            sentencia = []
        elif limpia.startswith("--"):
            continue
        elif limpia:
            sentencia.append(limpia)

    if nombre is not None:
        consultas[nombre] = " ".join(sentencia).strip()

    return consultas


# Consultas cargadas desde gastos.sql, con alias cortos para no escribir
# CONSULTAS["..."] en cada función. El texto SQL proviene 100% del archivo.
CONSULTAS = _leer_consultas()
SQL_INSERTAR_GASTO = CONSULTAS["insertar_gasto"]
SQL_TOTAL_POR_CATEGORIA = CONSULTAS["total_por_categoria"]
SQL_TOTAL_GENERAL = CONSULTAS["total_general"]
SQL_GASTOS_POR_CATEGORIA = CONSULTAS["gastos_por_categoria"]
SQL_LISTAR_GASTOS = CONSULTAS["listar_gastos"]
SQL_OBTENER_GASTO = CONSULTAS["obtener_gasto"]
SQL_ACTUALIZAR_GASTO = CONSULTAS["actualizar_gasto"]
SQL_ELIMINAR_GASTO = CONSULTAS["eliminar_gasto"]
SQL_PRESUPUESTOS = CONSULTAS["presupuestos"]


def conectar() -> sqlite3.Connection:
    """Abre una conexión, crea las tablas si no existen y la devuelve.

    Al conectar se ejecuta el esquema (CREATE TABLE e INSERT de
    presupuestos). Es idempotente: si la base ya existe, las sentencias
    `IF NOT EXISTS` / `OR IGNORE` no alteran nada.
    """
    conexion = sqlite3.connect(RUTA_DB)
    conexion.executescript(_leer_esquema())
    conexion.commit()
    return conexion


def insertar_gasto(categoria, monto, descripcion):
    """Inserta un gasto y devuelve el id que le asignó la base."""
    with conectar() as conexion:
        cursor = conexion.execute(SQL_INSERTAR_GASTO, (categoria, monto, descripcion))
        print(f"Insertar Gasto, categoria = {categoria}, monto = {monto}, descripcion = {descripcion} ")
    return cursor.lastrowid


def total_por_categoria(categoria):
    """Suma los montos de una categoría (0 si no hay gastos)."""
    with conectar() as conexion:
        fila = conexion.execute(SQL_TOTAL_POR_CATEGORIA, (categoria,)).fetchone()
    # COALESCE hace que la suma nunca sea NULL; igual chequeamos por si
    # la consulta no devuelve ninguna fila.
    return fila[0] if fila is not None else 0.0


def total_general():
    """Suma todos los gastos registrados."""
    with conectar() as conexion:
        fila = conexion.execute(SQL_TOTAL_GENERAL).fetchone()
    return fila[0] if fila is not None else 0.0


def gastos_por_categoria():
    """Devuelve {categoria: total_gastado} usando GROUP BY."""
    with conectar() as conexion:
        filas = conexion.execute(SQL_GASTOS_POR_CATEGORIA).fetchall()
    return dict(filas)


def listar_gastos():
    """Devuelve todas las filas de la tabla gastos, la más nueva primero.

    Cada fila es una tupla (id, categoria, monto, descripcion, fecha).
    """
    with conectar() as conexion:
        return conexion.execute(SQL_LISTAR_GASTOS).fetchall()


def obtener_gasto(id_gasto):
    """Trae un solo gasto por id, o None si no existe.

    Devuelve una tupla (id, categoria, monto, descripcion, fecha).
    """
    with conectar() as conexion:
        return conexion.execute(SQL_OBTENER_GASTO, (id_gasto,)).fetchone()


def actualizar_gasto(id_gasto, categoria, monto, descripcion):
    """Modifica un gasto existente.

    Devuelve la cantidad de filas modificadas (1 si actualizó, 0 si el
    id no existe).
    """
    with conectar() as conexion:
        cursor = conexion.execute(
            SQL_ACTUALIZAR_GASTO, (categoria, monto, descripcion, id_gasto)
        )
    return cursor.rowcount


def eliminar_gasto(id_gasto):
    """Borra un gasto por id.

    Devuelve la cantidad de filas borradas (1 si eliminó, 0 si el id no
    existe).
    """
    with conectar() as conexion:
        cursor = conexion.execute(SQL_ELIMINAR_GASTO, (id_gasto,))
    return cursor.rowcount


def presupuestos():
    """Devuelve {categoria: presupuesto} desde la tabla presupuestos."""
    with conectar() as conexion:
        filas = conexion.execute(SQL_PRESUPUESTOS).fetchall()
    return dict(filas)