# Ejercicio 1 — Planilla de calificaciones que se guarda

> **Migración de:** TP 5 — Calificaciones (`../../ejercicios3/tp05_calificaciones.md`)
> **Conceptos nuevos:** leer y escribir un archivo de texto desde una ventana
> (`open` con `with`, `readlines`, `write`), parsear líneas con `split(";")` y
> `try/except` para el archivo y los valores.

## Punto de partida

El archivo `ejercicio01_calificaciones.py` ya trae la **ventana inicial armada**: los
widgets, sus tags (`input_alumno`, `input_nota`, `panel_notas`, `txt_estado`, ...) y
los botones conectados a los callbacks. Tu trabajo es completar el resto:

1. Crear el módulo `modulos/servicio_notas.py` con la lógica que describe el enunciado
   (carga del archivo, alta de notas, resumen, guardado) y las funciones de la "Pista".
2. Completar los callbacks en `ejercicio01_calificaciones.py` para que lean la interfaz
   con `dpg.get_value(...)`, llamen a las funciones del módulo y actualicen los widgets
   con `dpg.set_value(...)`.

Al ejecutar el archivo, la ventana abre sin errores pero los botones **todavía no hacen
nada**: se activan cuando implementes la lógica y los callbacks.

## La situación

Soy profesor y tengo que llevar las notas de mi curso. Hasta ahora las tenía en un
cuaderno, pero se me enredan. Quiero una ventana donde pueda ir **cargando cada alumno
con su nota**, ir viendo la lista mientras la armo, y que me **guarde todo en un
archivo** para que la próxima vez que abra el programa aparezcan las notas que ya cargué.
No quiero volver a tipearlas nunca más.

## Lo que necesito que haga el programa

1. Dos **campos de texto**: uno para el nombre del **alumno** y otro para la **nota**.
2. Botón **Agregar nota**: valida los datos y agrega al alumno con su nota. Un panel
   muestra la lista de alumnos con sus notas, actualizándose en cada carga.
3. Botón **Ver resumen**: muestra en un área de texto (multilínea de solo lectura) un
   informe con el **promedio** del curso, cuántos **aprobaron** (nota mayor o igual a 6)
   y cuántos **desaprobaron**, la **nota más alta** con el nombre del alumno, y la
   **cantidad total** de alumnos cargados.
4. Botón **Guardar**: escribe todas las notas en el archivo `notas.txt`.
5. Al **iniciar**, el programa lee `notas.txt`. Si el archivo no existe todavía, arranca
   vacío, sin romperse.
6. Un **texto de estado** que avise si la nota se cargó o qué salió mal.

## Detalles importantes

- El **archivo** tiene una línea por alumno con el formato `alumno;nota`, por ejemplo
  `Ana;8`. La carga y el guardado se hacen **en el módulo** de lógica, nunca en la
  ventana.
- **No se pueden repetir nombres** de alumnos: si cargo un nombre que ya está, el
  programa avisa y no lo agrega otra vez.
- La **nota llega como texto** (viene de la GUI): casteala con `try/except` y además
  aceptá el signo `,` como separador decimal (`7,5` y `7.5` valen igual). Solo se
  aceptan notas entre **1 y 10**.
- Al terminar una acción exitosa, los **campos se limpian** para cargar el siguiente
  alumno.
- El panel de la lista se redibuja borrando sus hijos con
  `dpg.delete_item("panel_notas", children_only=True)` y agregando el texto nuevo.

## Pista de qué conceptos entran en juego

Un diccionario `alumno → nota` como estado, funciones que devuelven `(ok, mensaje)`,
`sum()` y `len()` para el promedio, `max()` sobre los valores del diccionario para la
mejor nota, `open(..., "r")` / `open(..., "w")` con `with` para el archivo,
`readlines()` y `split(";")` para leer, y un `try/except` que cubra también el caso de
que el archivo no exista.

## Cómo ejecutarlo

Desde la carpeta de este ejercicio:

```bash
python ejercicio01_calificaciones.py
```