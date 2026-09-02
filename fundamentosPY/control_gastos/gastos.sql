-- =====================================================================
-- SENTENCIAS SQL - Ejemplo "Control de gastos" (SQLite)
-- ---------------------------------------------------------------------
-- ESTE ARCHIVO ES LA ÚNICA FUENTE DE VERDAD DE LAS SENTENCIAS SQL.
-- El módulo `modulos/base_datos.py` lo lee con la biblioteca nativa
-- `sqlite3` y ejecuta lo que contiene, en dos zonas:
--
--   ZONA 1 - ESQUEMA: se ejecuta al arrancar la app (CREATE TABLE e
--   INSERT de presupuestos).
--   ZONA 2 - CONSULTAS: consultas parametrizadas del día a día. Python
--   las parsea y las ejecuta con parámetros (?). Por eso NO se pueden
--   correr a mano desde la terminal: los "?" se reemplazan con valores
--   desde Python.
--
-- Para cambiar o agregar una sentencia, editá este archivo: la app lo
-- toma automáticamente sin tocar código.
-- =====================================================================


-- =====================================================================
-- ZONA 1 - ESQUEMA (DDL + datos iniciales)
-- Marcamos inicio y fin para que Python extraiga este bloque y lo
-- ejecute con `executescript()`.
-- =====================================================================
-- ===INICIO ESQUEMA===

-- Tabla de presupuestos por categoría.
-- La columna `categoria` es la CLAVE PRIMARIA: no pueden existir
-- dos categorías con el mismo nombre.
CREATE TABLE IF NOT EXISTS presupuestos (
    categoria   TEXT    PRIMARY KEY,     -- nombre de la categoría
    presupuesto REAL    NOT NULL         -- tope de gasto mensual en $
);

-- Tabla de gastos registrados.
-- `id` se genera solo (AUTOINCREMENT), `fecha` se guarda sola con la
-- hora actual del sistema. `monto` es REAL (número con decimales).
CREATE TABLE IF NOT EXISTS gastos (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria   TEXT    NOT NULL,
    monto       REAL    NOT NULL,
    descripcion TEXT    NOT NULL,
    fecha       TEXT    DEFAULT (datetime('now', 'localtime'))
);

-- Datos iniciales de presupuestos (solo se insertan si no existen,
-- por eso usamos INSERT OR IGNORE).
INSERT OR IGNORE INTO presupuestos (categoria, presupuesto) VALUES
    ('comida',     50000.0),
    ('transporte', 20000.0),
    ('ocio',       15000.0);

-- ===FIN ESQUEMA===


-- =====================================================================
-- ZONA 2 - CONSULTAS PARAMETRIZADAS
-- Cada consulta se identifica con un marcador `-- @nombre` y termina
-- con ";". `base_datos.py` las parsea en el diccionario `CONSULTAS`
-- usando ese nombre.
--
-- Los "?" son marcadores de posición: los valores se pasan por
-- separado (nunca concatenados), así evitamos la INYECCIÓN SQL.
-- =====================================================================
-- ===INICIO CONSULTAS===

-- @insertar_gasto
-- Registra un gasto nuevo. Los "?" se reemplazan por
-- (categoria, monto, descripcion).
INSERT INTO gastos (categoria, monto, descripcion)
VALUES (?, ?, ?);

-- @total_por_categoria
-- Suma cuánto se gastó en una categoría concreta.
-- COALESCE evita que la suma dé NULL cuando no hay gastos.
SELECT COALESCE(SUM(monto), 0)
FROM gastos
WHERE categoria = ?;

-- @total_general
-- Suma el gasto total (todas las categorías).
SELECT COALESCE(SUM(monto), 0)
FROM gastos;

-- @gastos_por_categoria
-- Suma el gasto de cada categoría (agrupado por categoría).
-- Sirve para armar el resumen por filas.
SELECT categoria, COALESCE(SUM(monto), 0)
FROM gastos
GROUP BY categoria;

-- @listar_gastos
-- Lista todos los gastos del más reciente al más antiguo.
SELECT id, categoria, monto, descripcion, fecha
FROM gastos
ORDER BY fecha DESC, id DESC;

-- @obtener_gasto
-- Trae UN solo gasto por su id (para cargarlo en el formulario).
SELECT id, categoria, monto, descripcion, fecha
FROM gastos
WHERE id = ?;

-- @actualizar_gasto
-- Modifica categoría, monto y descripción de un gasto existente.
-- El WHERE por id evita tocar otras filas.
UPDATE gastos
SET categoria = ?, monto = ?, descripcion = ?
WHERE id = ?;

-- @eliminar_gasto
-- Borra un gasto por su id.
DELETE FROM gastos
WHERE id = ?;

-- @presupuestos
-- Lee los presupuestos guardados en la base.
SELECT categoria, presupuesto
FROM presupuestos;

-- ===FIN CONSULTAS===