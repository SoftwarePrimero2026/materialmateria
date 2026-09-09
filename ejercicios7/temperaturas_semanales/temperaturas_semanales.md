# Ejercicio 1 — Registro de temperaturas semanales que se guarda (SQLite)

> **Migración de:** TP 4 — Temperaturas semanales (`../../ejercicios3/tp04_temperaturas_semanales.md`)
> **Conceptos nuevos:** guardar los datos en una **base de datos SQLite** con la
> biblioteca nativa `sqlite3` (sin ORM). La base se **genera sola** desde un archivo
> `.sql` (esquema + datos iniciales), los registros se **guardan** con `INSERT` y se
> **consultan** con `SELECT`.

## Punto de partida

El archivo `temperaturas_semanales.py` ya trae la **ventana inicial armada**:
los widgets, sus tags (`input_dia`, `input_temp_max`, `input_temp_min`,
`panel_registros`, `txt_estado`, `txt_resumen`, ...) y los botones conectados a los
callbacks. Tu trabajo es completar el resto:

1. Crear el archivo **`temperaturas.sql`** con TODAS las sentencias SQL del proyecto
   (esquema de la tabla con sus datos iniciales + consultas parametrizadas), siguiendo el
   patrón de `fundamentosPY/control_gastos/gastos.sql` (marcadores
   `-- ===INICIO ESQUEMA===` / `-- ===FIN ESQUEMA===` y consultas marcadas con
   `-- @nombre`).
2. Crear el módulo **`modulos/base_datos.py`** con el acceso a SQLite: la conexión que
   ejecuta el esquema al conectar y una función por cada consulta parametrizada.
3. Crear el módulo **`modulos/servicio_temperaturas.py`** con la lógica que describe el
   enunciado (validaciones, registrar día, listar registros, resumen) y las funciones de
   la "Pista".
4. Completar los **callbacks** en `temperaturas_semanales.py` para que lean
   la interfaz con `dpg.get_value(...)`, llamen a las funciones del módulo y actualicen
   los widgets con `dpg.set_value(...)`.

Al ejecutar el archivo, la ventana abre sin errores pero los botones **todavía no hacen
nada**: se activan cuando implementes la lógica y los callbacks.

## La situación

Soy meteorólogo aficionado y quiero llevar el registro de las temperaturas de la semana.
Hasta ahora anotaba en un papel la **máxima** y la **mínima** de cada día, pero se me
pierde y encima me cuesta sacar los promedios. Quiero una ventana donde pueda ir
**cargando cada día con sus dos temperaturas**, ir viendo la lista mientras la armo, y
que **todo quede guardado en una base de datos** para que la próxima vez que abra el
programa aparezcan los días que ya cargué. No quiero volver a tipearlos nunca más.

## Lo que necesito que haga el programa

1. Un **combo** para elegir el día de la semana (Lunes a Domingo) y dos **campos de
   texto**: temperatura **máxima** y temperatura **mínima**.
2. Botón **Registrar día**: valida los datos y **guarda el registro en la base de datos**.
   Un panel muestra los días cargados con sus temperaturas (máx, mín y amplitud),
   actualizándose en cada alta.
3. Botón **Ver resumen**: muestra en un área de texto (multilínea de solo lectura) un
   informe con:
   - el **promedio** de las máximas y el **promedio** de las mínimas,
   - el **día más caluroso** (mayor máxima) y el **día más frío** (menor mínima),
   - los **días con amplitud térmica mayor a un umbral** (por ejemplo 12°C).
4. Al **iniciar**, el programa **genera la base de datos si no existe**: ejecuta el
   esquema desde `temperaturas.sql` (tabla + datos iniciales) y **carga los registros
   que ya estén guardados**, sin romperse si es la primera vez.
5. Un **texto de estado** que avise si el día se registró o qué salió mal.

## Detalles importantes

- **TODAS las sentencias SQL viven en `temperaturas.sql`** (única fuente de verdad): la
  app no arma SQL dentro del código Python; lo lee del archivo y lo ejecuta.
- La base de datos se llama **`temperaturas.db`** y **se crea sola** en la primera
  ejecución, en la misma carpeta del ejercicio.
- Las consultas que llevan valores se hacen con **parámetros `?`** (nunca concatenando
  texto en la cadena SQL), para evitar la **inyección SQL**.
- **No se puede registrar dos veces el mismo día**: si elijo un día que ya está cargado,
  el programa avisa y no lo agrega otra vez. Tip: la columna `dia` puede ser la clave
  primaria o tener `UNIQUE`.
- Las temperaturas **llegan como texto** (vienen de la GUI): castealas con `try/except`
  y aceptá el signo `,` como separador decimal (`28,5` y `28.5` valen igual). Validá que
  la **máxima sea mayor o igual que la mínima** y que no sea un día vacío.
- Al terminar una acción exitosa, los **campos se limpian** para cargar el siguiente día.
- El panel de la lista se redibuja borrando sus hijos con
  `dpg.delete_item("panel_registros", children_only=True)` y agregando el texto nuevo.

## Pista de qué conceptos entran en juego

En la capa de datos (`base_datos.py`): `sqlite3.connect()` para abrir/crear la base,
`executescript()` para correr el esquema del `.sql` (CREATE TABLE + INSERT de datos
iniciales), `execute()` con parámetros `?` para INSERT y SELECT, `fetchone()` /
`fetchall()` para leer los resultados y `COALESCE` para que promedios y sumas no den
`NULL` cuando todavía no hay registros. En la capa de servicio
(`servicio_temperaturas.py`): funciones que devuelven `(ok, mensaje)` igual que en
`ejercicios5` / `ejercicios6`. Para el resumen, `AVG()` sobre cada columna, y el día más
caluroso / más frío se pueden resolver con `ORDER BY` + `LIMIT 1` o calculando en Python
sobre la lista cargada. Todo el patrón de capas está explicado y funcionando en
`fundamentosPY/control_gastos/` (lectura recomendada antes de arrancar).

## Cómo ejecutarlo

Desde la carpeta de este ejercicio:

```bash
python temperaturas_semanales.py
```
