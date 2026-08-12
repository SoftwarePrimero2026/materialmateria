# Ejercicio 2 — Simulador de caja registradora con ticket

> **Migración de:** TP 10 — Simulador de caja registradora (`../../ejercicios3/tp10_caja_registradora.md`)
> **Widgets Nuevos:** `dpg.add_input_text(..., multiline=True, readonly=True)`,
> refrescar paneles con `dpg.delete_item` + `dpg.add_text`, `dpg.add_separator`.

## Punto de partida

El archivo `ejercicio02_caja_registradora.py` ya trae la **ventana inicial armada**:
los widgets, sus tags (`input_nombre`, `input_categoria`, `input_precio`,
`panel_productos`, `txt_ticket`, ...) y los botones conectados a los callbacks. Tu trabajo
es completar el resto:

1. Crear el módulo `modulos/servicio_caja.py` con la lógica que describe el enunciado
   (lista de tuplas, descuentos, ticket) y las funciones de la "Pista".
2. Completar los callbacks en `ejercicio02_caja_registradora.py` para que lean la interfaz
   con `dpg.get_value(...)`, llamen a las funciones del módulo y actualicen los widgets con
   `dpg.set_value(...)`.

Al ejecutar el archivo, la ventana abre sin errores pero los botones **todavía no hacen
nada**: se activan cuando implementes la lógica y los callbacks. La versión resuelta queda
guardada en la carpeta `resuelta/` como referencia.

## La situación

En el TP 10 construiste una caja registradora que cargaba productos por consola y
emitía un ticket con descuentos. Ahora hay que pasarla a una ventana: el operador
completa **producto, categoría y precio** en la pantalla, aprieta un botón, y el
programa va acumulando la compra. Con otro botón genera el **ticket formateado**.

## Lo que necesito que haga el programa

1. Tres **campos de texto**: producto, categoría y precio.
2. Botón **Agregar producto**: valida los datos y los agrega a la compra. Un panel
   muestra la lista de productos cargados, actualizándose en cada carga.
3. Botón **Generar ticket**: muestra, en un área de texto (multilínea de solo lectura),
   el ticket formateado con bordes Unicode: subtotal, descuentos por categoría, total y
   cantidad de categorías compradas.
4. Botón **Nueva compra**: vacía todo para empezar otro ticket.
5. Un **texto de estado** que avise si el producto se cargó o qué salió mal.

## Detalles importantes

- El **precio llega como texto** (viene de la GUI): castealo con `try/except` y además
  aceptame el signo `,` como separador decimal (`350,50` y `350.50` valen igual).
- Solo se agregan productos con nombre, categoría y precio **mayor a cero**.
- Si la categoría **no está** en el diccionario de descuentos, el producto se incluye
  igual pero sin descuento.
- Toda la lógica (validación, subtotal, descuentos, ticket) debe vivir en el módulo
  `modulos/servicio_caja.py`. La ventana solo conecta widgets con funciones.

## Pista de qué conceptos entran en juego

Lista de tuplas `(nombre, categoria, precio)` como estado, diccionario de descuentos,
conjunto para las categorías únicas, `try/except` para el precio, una función que arma
el ticket como **cadena** (en vez de `print`), y una única función `refrescar_productos()`
que borra el panel y lo vuelve a dibujar.

## Cómo ejecutarlo

Desde la carpeta de este ejercicio:

```bash
python ejercicio02_caja_registradora.py
```