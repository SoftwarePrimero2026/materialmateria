# Ejercicio 1 — Lista de compras con interfaz gráfica

> **Migración de:** TP 1 — Gestión de lista de compras (`../../ejercicios3/tp01_lista_de_compras.md`)
> **Widgets Nuevos:** `dpg.add_window`, `dpg.add_input_text`, `dpg.add_button`,
> `dpg.add_child_window`, callbacks, `dpg.set_value` / `dpg.get_value`,
> `dpg.delete_item(..., children_only=True)`.

## Punto de partida

El archivo `ejercicio01_lista_compras.py` ya trae la **ventana inicial armada**:
los widgets, sus tags (`input_item`, `txt_estado`, `panel_resumen`, ...) y los botones
conectados a los callbacks. Tu trabajo es completar el resto:

1. Crear el módulo `modulos/servicio_compras.py` con la lógica que describe el enunciado
   (lista de pendientes + conjunto de comprados y las funciones de la "Pista").
2. Completar los callbacks en `ejercicio01_lista_compras.py` para que lean la interfaz con
   `dpg.get_value(...)`, llamen a las funciones del módulo y actualicen los widgets con
   `dpg.set_value(...)`.

Al ejecutar el archivo, la ventana abre sin errores pero los botones **todavía no hacen
nada**: se activan cuando implementes la lógica y los callbacks. La versión resuelta queda
guardada en la carpeta `resuelta/` como referencia.

## La situación

Ya sabés manejar listas, conjuntos y funciones en la consola (lo hiciste en el TP 1).
Ahora el cliente quiere lo mismo pero **sin escribir comandos**: quiere una ventana con
campos para escribir, botones para presionar y un panel que muestre la lista siempre
actualizada.

## Lo que necesito que haga el programa

Creá una ventana de Dear PyGui que replique la lista de compras del TP 1:

1. Un **campo de texto** donde se escribe el nombre del ítem.
2. Tres **botones**:
   - **Agregar ítem**: suma el ítem a la lista pendiente.
   - **Marcar como comprado**: mueve el ítem al conjunto de comprados.
   - **Eliminar ítem**: lo saca de la lista pendiente.
3. Un **panel** (ventana hija) que muestre el resumen formateado: pendientes y ya
   comprados, con sus cantidades. El panel se **actualiza solo** después de cada acción.
4. Un **texto de estado** que avise qué pasó con la última acción (por ejemplo,
   `'Leche' fue agregado correctamente.` o `'X' ya está en la lista de compras.`).

## Detalles importantes

- La lógica debe estar **en un módulo aparte** (`modulos/servicio_compras.py`), nunca
  mezclada con la interfaz. Cada función devuelve `(ok, mensaje)` para que la ventana
  decida qué mostrar.
- **No se pueden agregar duplicados** y no se puede marcar/eliminar un ítem inexistente.
- Al terminar una acción exitosa, el **campo de texto se limpia** para poder escribir el
  siguiente ítem.
- El panel de resumen se redibuja borrando sus hijos con
  `dpg.delete_item("panel_resumen", children_only=True)` y agregando el texto nuevo.

## Pista de qué conceptos entran en juego

Callbacks que leen la interfaz con `dpg.get_value(...)` y la actualizan con
`dpg.set_value(...)`, una función por acción, una lista + un conjunto como estado,
y una función `actualizar_paneles()` que evita repetir código en los tres callbacks.

## Cómo ejecutarlo

Desde la carpeta de este ejercicio:

```bash
python ejercicio01_lista_compras.py
```