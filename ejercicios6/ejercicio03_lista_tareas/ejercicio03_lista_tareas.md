# Ejercicio 3 — Lista de tareas con estados y guardado

> **Migración de:** ejercicio nuevo, combina lo visto en la lista de compras
> (`../../ejercicios5/ejercicio01_lista_compras`) con el manejo de archivos.
> **Widgets Nuevos:** `dpg.add_combo` para elegir el estado de la tarea.

## Punto de partida

El archivo `ejercicio03_lista_tareas.py` ya trae la **ventana inicial armada**: los
widgets, sus tags (`input_tarea`, `combo_estado`, `panel_tareas`, `txt_estado`, ...) y
los botones conectados a los callbacks. Tu trabajo es completar el resto:

1. Crear el módulo `modulos/servicio_tareas.py` con la lógica que describe el enunciado
   (carga del archivo, alta, avance de estado, eliminación, listado, guardado) y las
   funciones de la "Pista".
2. Completar los callbacks en `ejercicio03_lista_tareas.py` para que lean la interfaz
   con `dpg.get_value(...)`, llamen a las funciones del módulo y actualicen los widgets
   con `dpg.set_value(...)`.

Al ejecutar el archivo, la ventana abre sin errores pero los botones **todavía no hacen
nada**: se activan cuando implementes la lógica y los callbacks.

## La situación

Me cuesta organizarme con las cosas que tengo que hacer en la semana. Quiero una ventana
donde pueda **anotar mis tareas** y cambiarles el **estado**: pendiente, en curso o
completada. Y lo más importante: quiero que la lista **quede guardada** para no tener
que volver a escribirla cada vez que abro el programa.

## Lo que necesito que haga el programa

1. Un **campo de texto** para la descripción de la tarea.
2. Un **combo** (`add_combo`) para elegir el **estado** inicial de la tarea, con las
   opciones `pendiente`, `en curso` y `completada`.
3. Botón **Agregar tarea**: agrega la tarea con el estado elegido.
4. Botón **Avanzar estado**: toma la tarea escrita en el campo y la pasa al siguiente
   estado (`pendiente` → `en curso` → `completada`). Si ya está completada, avisa que no
   puede avanzar más.
5. Botón **Eliminar tarea**: la saca de la lista.
6. Un **panel** que muestre las tareas **agrupadas por estado** (Pendientes, En curso,
   Completadas) con la cantidad de cada grupo y el total de tareas **completadas**.
   El panel se actualiza después de cada acción.
7. Botón **Guardar**: escribe la lista en `tareas.txt`.
8. Al **iniciar**, el programa lee `tareas.txt`. Si el archivo no existe, arranca vacío,
   sin romperse.
9. Un **texto de estado** que avise el resultado de cada acción.

## Detalles importantes

- El **archivo** tiene una línea por tarea con el formato `descripcion;estado`, por
  ejemplo `Estudiar para el parcial;pendiente`. La carga y el guardado se hacen **en el
  módulo** de lógica.
- **No se permiten tareas duplicadas**: si cargo una descripción que ya está, el
  programa avisa y no la agrega otra vez.
- Los **estados válidos** son exactamente los tres: `pendiente`, `en curso` y
  `completada`. El combo trae esas opciones y el módulo igual debe controlar que un
  estado venga de ahí.
- Al **avanzar estado**, la descripción se busca tal cual está en la lista; si la tarea
  no existe, se avisa sin romperse.
- El panel se redibuja borrando sus hijos con
  `dpg.delete_item("panel_tareas", children_only=True)` y agregando el texto nuevo.

## Pista de qué conceptos entran en juego

Una lista de tuplas `(descripcion, estado)` como estado, un diccionario o `if/elif`
para saber cuál es el "siguiente estado", recorridos que armen el texto agrupando por
estado, `open(..., "r")` / `open(..., "w")` con `with` y `split(";")` para el archivo,
funciones que devuelven `(ok, mensaje)`, y una función `refrescar_panel()` que evita
repetir código en los callbacks.

## Cómo ejecutarlo

Desde la carpeta de este ejercicio:

```bash
python ejercicio03_lista_tareas.py
```