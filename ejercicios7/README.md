# Ejercicios 7 — Ventanas con datos en una base SQL (SQLite)

Bienvenidos a la séptima tanda de ejercicios. En `ejercicios5` llevaste programas de la
consola a una **ventana con Dear PyGui** y separaste la lógica en módulos
(`modulos/servicio_*.py`). En `ejercicios6` los datos dejaron de perderse al cerrar la
ventana porque pasaste a **guardarlos en un archivo de texto**. Esta tanda da el último
paso: **guardar los datos en una base de datos SQLite** usando solo la biblioteca nativa
`sqlite3` de Python (sin ORM, sin dependencias extra).

La idea central es la **base de datos**: la ventana se ve igual que en las tandas
anteriores, pero ahora los datos viven en una tabla. El programa **genera la base sola**
al iniciar (el esquema y los datos iniciales se definen con sentencias SQL), **guarda**
cada registro con un `INSERT` y **consulta** la información con `SELECT` para mostrar la
lista y los resúmenes. Ya no hay `open()/readlines()/write()`: todo lo que antes era un
archivo de texto ahora es una tabla.

## Requisitos

- Python 3.10 o superior.
- El paquete `dearpygui`:

```bash
pip install dearpygui
```

> La base de datos **no necesita instalar nada**: `sqlite3` viene incluido en Python.

## Referencia: el ejemplo `control_gastos`

En `fundamentosPY/control_gastos/` hay un **ejemplo completo y resuelto** que usa esta
misma arquitectura (interfaz + lógica + base de datos SQLite). Leelo y corrélo **antes**
de empezar para ver el patrón en acción:

- `control_gastos.py` → interfaz gráfica (Dear PyGui).
- `gastos.sql` → **todas** las sentencias SQL (esquema + consultas), única fuente de verdad.
- `modulos/base_datos.py` → acceso a SQLite (solo `sqlite3`, sin ORM).
- `modulos/servicio_gastos.py` → lógica de negocio y validaciones.

> **Ojo:** el ejemplo es la *referencia*, no la solución del ejercicio. Copiá el
> **patrón** (la estructura de capas y cómo se organiza el SQL) pero resolvé el problema
> del enunciado con tus propias sentencias y funciones.

## ¿Qué tenés que hacer?

En esta carpeta vas a encontrar **1 ejercicio** (una carpeta por ejercicio). Cada carpeta
contiene:

- El **enunciado** (`.md`): explica todo lo que el programa debe hacer, contado como si
  te estuvieran pidiendo el programa.
- El **punto de partida** (`.py`): la ventana ya armada con los widgets, tags y botones
  conectados a callbacks vacíos. Apenas abre pero **los botones todavía no hacen nada**.

| Ejercicio                  | Migra de                      | Qué construís                                                                    |
| -------------------------- | ----------------------------- | ---------------------------------------------------------------------------------- |
| `temperaturas_semanales` | TP 4 (temperaturas semanales) | Registro diario de máx/mín con resumen estadístico, guardado en una base SQLite |

Tu tarea por ejercicio es:

1. **Crear el archivo `.sql`** con TODAS las sentencias SQL del proyecto (el esquema de
   la tabla con sus datos iniciales y las consultas parametrizadas), siguiendo el patrón
   de marcadores de `gastos.sql`.
2. **Crear la lógica** en un módulo (`modulos/servicio_*.py`), separada de la interfaz,
   con las validaciones y las funciones que devuelven `(ok, mensaje)`.
3. **Crear el acceso a datos** en `modulos/base_datos.py`: la conexión que ejecuta el
   esquema al iniciar y una función por cada consulta parametrizada.
4. **Completar los callbacks** del `.py` de partida para que lean la interfaz con
   `dpg.get_value(...)`, llamen a tu módulo y actualicen los widgets con
   `dpg.set_value(...)`.

Mismo patrón que siempre, pero ahora con **tres capas**: **interfaz en la ventana**,
**lógica en el servicio**, **datos en la base**.

## ¿Qué conceptos vas a necesitar?

- **Dear PyGui**: `create_context`, `create_viewport`, `setup_dearpygui`,
  `show_viewport`, `start_dearpygui`, `destroy_context`, ventanas y su ciclo de vida.
- **Widgets**: `add_text`, `add_input_text`, `add_combo`, `add_button`,
  `add_child_window`, `add_separator`, `add_spacer`.
- **Comunicación con la interfaz**: `dpg.get_value(...)`, `dpg.set_value(...)`,
  `dpg.delete_item(..., children_only=True)` para refrescar paneles.
- **SQLite con `sqlite3`**: `sqlite3.connect()`, `executescript()` para ejecutar el
  esquema, `execute()` con parámetros `?`, `fetchone()` / `fetchall()`, `commit()`.
- **SQL básico**: `CREATE TABLE IF NOT EXISTS`, `INSERT`, `SELECT`, `WHERE`,
  `ORDER BY`, `GROUP BY`, `SUM` / `AVG`, `COALESCE`.
- **Seguridad**: consultas siempre **parametrizadas** con `?` (nunca concatenando texto)
  para evitar la inyección SQL.
- **Manejo de errores**: `try/except` tanto para los valores que llegan de la GUI como
  para el caso de que la base no exista todavía (aunque la app la crea sola).
- **Callbacks** y la **separación de responsabilidades** de las tandas anteriores.
- Y todo lo anterior del curso: listas, diccionarios, tuplas, funciones, ciclos y
  f-strings.

## ¿Qué se va a evaluar?

1. **Comprensión del problema**: que la ventana haga todo lo que pide el enunciado.
2. **Base de datos correcta**: que el esquema se cree solo al iniciar, que los datos se
   **guarden** y se **carguen** al reabrir la app, sin perder ni duplicar información.
3. **SQL en un archivo**: que todas las sentencias vivan en el `.sql` (única fuente de
   verdad) y que las consultas con valores usen parámetros `?`.
4. **Uso correcto del patrón**: lógica en `modulos/servicio_*.py`, acceso a datos en
   `modulos/base_datos.py`, interfaz en el `.py` principal, callbacks bien conectados.
5. **Validación y manejo de errores**: que el programa no se rompa si se ingresa un
   dato inválido, un campo vacío, un día repetido, o si la base no existe.
6. **Claridad del código**: nombres descriptivos, código ordenado y comentado.
7. **Interfaz usable**: los mensajes de estado explican qué pasó en cada acción y los
   paneles se actualizan correctamente.

## Forma de entrega

Por **cada ejercicio** entregá:

1. **Diagrama de flujo**: la lógica de tu solución (igual que en ejercicios anteriores).
2. **Código comentado**: tu carpeta con el `.py` principal, el `.sql`, y el `modulos/`,
   comentados, que ejecute sin errores.

> **Sugerencia de organización**: trabajá dentro de la carpeta de cada ejercicio
> completando el `.py` de partida y creando tu `modulos/` y tu `.sql`. La base de datos
> (`*.db`) se crea sola en la misma carpeta al ejecutar el programa; no hace falta
> entregarla.

## Cómo ejecutar cada ejercicio

Entrá a la carpeta del ejercicio y ejecutá el archivo principal, por ejemplo:

```bash
cd temperaturas_semanales
python temperaturas_semanales.py
```

¡Mucho éxito! Lo importante de esta tanda es entender **cómo se conecta una ventana con
una base de datos**: la interfaz pregunta, el servicio decide y la base responde.
