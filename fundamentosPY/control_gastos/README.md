# Ejemplo — Control de gastos con Python + SQLite (sin ORM)

Este proyecto es un **ejemplo completo y resuelto** de cómo integrar una aplicación de
escritorio con Dear PyGui a una base de datos **SQLite usando solo la biblioteca nativa
`sqlite3`** de Python (sin ORM, sin dependencias extra).

A diferencia de los ejercicios de `ejercicios5` / `ejercicios6`, acá **no hay nada que
completar**: el código está terminado y funcionando. La idea es que lo leas, lo corras y
lo uses como referencia para aprender el patrón de integración con bases de datos.

## ¿Qué hace la app?

Un control de gastos personales con **CRUD completo**:

| Operación | Qué hace |
|-----------|----------|
| **C**rear | Registrar un gasto (categoría, monto, descripción) |
| **R**ead | Ver el resumen por categorías y la tabla de todos los gastos |
| **U**pdate | Editar un gasto existente desde la misma tabla |
| **D**elete | Eliminar un gasto |

Además alerta cuando una categoría **supera su presupuesto** mensual.

## Requisitos

- Python 3.10 o superior.
- El paquete `dearpygui`:

```bash
pip install dearpygui
```

> La base de datos **no necesita instalar nada**: `sqlite3` viene incluido en Python.

## Cómo ejecutar

Desde la carpeta del proyecto:

```bash
python control_gastos.py
```

En la primera ejecución se crea automáticamente el archivo `gastos.db` junto al proyecto,
con las tablas y los presupuestos iniciales. Si lo borrás, se vuelve a crear solo.

## Estructura del proyecto

```
control_gastos/
├── control_gastos.py        # Interfaz gráfica (Dear PyGui)
├── gastos.sql               # TODAS las sentencias SQL (única fuente de verdad)
├── modulos/
│   ├── __init__.py          # Marca a `modulos/` como paquete
│   ├── servicio_gastos.py   # Lógica de negocio: validaciones y (ok, mensaje)
│   └── base_datos.py        # Acceso a SQLite: conexión y ejecución de consultas
└── gastos.db                # Se genera solo al ejecutar (no versionar)
```

## La arquitectura: tres capas

```
dearpygui (control_gastos.py)
        │  lee widgets y muestra resultados
        ▼
servicio_gastos.py  ← valida los datos, arma los mensajes
        │  llama a funciones de base_datos
        ▼
base_datos.py       ← abre la conexión y ejecuta el SQL de gastos.sql
        │
        ▼
gastos.db (SQLite)
```

La regla de oro del ejemplo: **la interfaz nunca habla con SQLite directamente**. Cada
capa tiene una sola responsabilidad:

- **`control_gastos.py`**: solo lee widgets (`dpg.get_value`), llama a la lógica y muestra
  resultados (`dpg.set_value`, tablas, resumen). No sabe qué es una base de datos.
- **`servicio_gastos.py`**: decide qué operación hacer, valida la entrada y devuelve
  `(ok, mensaje)` para que la interfaz muestre algo útil.
- **`base_datos.py`**: la única capa que abre conexiones, crea tablas y ejecuta SQL.

## El rol de `gastos.sql`

Todo el SQL vive en **un solo archivo**, `gastos.sql`, dividido en dos zonas:

- **ZONA 1 — ESQUEMA**: `CREATE TABLE` e `INSERT` de presupuestos. `base_datos.py` la
  extrae entre los marcadores `-- ===INICIO ESQUEMA===` / `-- ===FIN ESQUEMA===` y la
  ejecuta con `executescript()` cada vez que la app arranca.
- **ZONA 2 — CONSULTAS**: las consultas del día a día (INSERT, SELECT, UPDATE, DELETE),
  cada una identificada con `-- @nombre`. `base_datos.py` las parsea en el diccionario
  `CONSULTAS`.

Si querés cambiar o agregar una sentencia, **se cambia solo en `gastos.sql`** y la app lo
toma automáticamente.

## Conceptos que enseña este ejemplo

1. **`sqlite3.connect()`** y el uso de `with ... as conexion:` para abrir y cerrar la
   conexión correctamente.
2. **Consultas parametrizadas**: los `?` se reemplazan con valores pasados por separado
   (`conexion.execute(SQL, (valor1, valor2))`). Nunca concatenamos strings, así evitamos
   la **inyección SQL**.
3. **`executescript()`** para correr varias sentencias del esquema de una vez, y
   `IF NOT EXISTS` / `INSERT OR IGNORE` para que sea seguro repetir la ejecución.
4. **`cursor.lastrowid`** (para saber el id del gasto recién insertado) y **`rowcount`**
   (para saber si un UPDATE/DELETE tocó alguna fila).
5. **`COALESCE(SUM(...), 0)`** para que una suma vacía devuelva `0` y no `NULL`.
6. La **separación en capas**, que es la forma profesional de organizar una app.

## Orden sugerido para leerlo

1. `gastos.sql`: primero las sentencias, porque son la "verdad" del proyecto.
2. `modulos/base_datos.py`: cómo Python lee y ejecuta esas sentencias.
3. `modulos/servicio_gastos.py`: cómo la lógica decide qué operación hacer.
4. `control_gastos.py`: cómo se conecta todo con la interfaz.

> **Nota sobre la fuente**: Dear PyGui usa por defecto una fuente bitmap que no dibuja
> acentos (ej. "Categoría"). Si los ves cortados, cargá una fuente TTF con `dpg.add_font`.