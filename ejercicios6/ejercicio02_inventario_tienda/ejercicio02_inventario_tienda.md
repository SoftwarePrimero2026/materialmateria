# Ejercicio 2 — Inventario de tienda con persistencia

> **Migración de:** TP 6 — Inventario de tienda (`../../ejercicios3/tp06_inventario_tienda.md`)
> **Conceptos nuevos:** leer y escribir un archivo de texto desde una ventana,
> aviso de **stock bajo** cuando una cantidad queda debajo de un umbral.

## Punto de partida

El archivo `ejercicio02_inventario_tienda.py` ya trae la **ventana inicial armada**:
los widgets, sus tags (`input_producto`, `input_cantidad`, `input_precio`,
`panel_productos`, `txt_estado`, ...) y los botones conectados a los callbacks. Tu
trabajo es completar el resto:

1. Crear el módulo `modulos/servicio_inventario.py` con la lógica que describe el
   enunciado (carga del archivo, alta, venta, reposición, total, guardado) y las
   funciones de la "Pista".
2. Completar los callbacks en `ejercicio02_inventario_tienda.py` para que lean la
   interfaz con `dpg.get_value(...)`, llamen a las funciones del módulo y actualicen
   los widgets con `dpg.set_value(...)`.

Al ejecutar el archivo, la ventana abre sin errores pero los botones **todavía no hacen
nada**: se activan cuando implementes la lógica y los callbacks.

## La situación

Tengo una tienda y necesito controlar lo que tengo en el depósito: cuántas unidades de
cada producto, a qué precio las vendo y cuándo me estoy quedando sin stock. Quiero una
ventana donde pueda **cargar productos**, **vender** y **reponer**, viendo siempre el
listado al día, y que todo quede **guardado en un archivo** para que no se me pierda
cuando apago la computadora.

## Lo que necesito que haga el programa

1. Tres **campos de texto**: producto, cantidad y precio.
2. Botón **Agregar producto**: da de alta un producto nuevo con su cantidad inicial y
   su precio. Si el producto ya existe, avisa y no lo duplica.
3. Botón **Vender**: resta unidades del producto (no puede quedar con cantidad
   negativa). Si no quedan suficientes, avisa.
4. Botón **Reponer**: suma unidades al producto.
5. Un **panel** que muestre el listado con nombre, cantidad, precio unitario y el
   **valor total del inventario** (suma de `cantidad * precio`), actualizándose después
   de cada acción. Los productos con **stock bajo** (menos unidades que un umbral
   definido en el código, por ejemplo 5) deben marcarse de alguna manera para que se
   noten.
6. Botón **Guardar**: escribe todo el inventario en `inventario.txt`.
7. Al **iniciar**, el programa lee `inventario.txt`. Si el archivo no existe, arranca
   vacío, sin romperse.
8. Un **texto de estado** que avise el resultado de cada acción.

## Detalles importantes

- El **archivo** tiene una línea por producto con el formato `producto;cantidad;precio`,
  por ejemplo `Harina;20;3500`. La carga y el guardado se hacen **en el módulo** de
  lógica, nunca en la ventana.
- La **cantidad** es un número **entero mayor o igual a cero**; el **precio** es un
  número **mayor a cero**. Ambos llegan como texto desde la GUI: castealos con
  `try/except` (y aceptá `,` como separador decimal en el precio).
- Al **vender**, la cantidad no puede quedar negativa; al **reponer**, siempre suma.
- El **umbral de stock bajo** se define en el código, dentro del módulo de lógica.
- El panel se redibuja borrando sus hijos con
  `dpg.delete_item("panel_productos", children_only=True)` y agregando el texto nuevo.

## Pista de qué conceptos entran en juego

Un diccionario `producto → (cantidad, precio)` como estado, funciones que devuelven
`(ok, mensaje)`, `try/except` para cantidad y precio, `open(..., "r")` / `open(..., "w")`
con `with` para el archivo, `split(";")` para leer, un `for` acumulador para el valor
total del inventario, y una única función `refrescar_productos()` que borra el panel y
lo vuelve a dibujar.

## Cómo ejecutarlo

Desde la carpeta de este ejercicio:

```bash
python ejercicio02_inventario_tienda.py
```