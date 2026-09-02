# Ejercicio 5 — Control de gastos personales con presupuesto

> **Migración de:** Ejercicio 4 — Control de gastos personales
> (`../../ejercicios4/ejercicio4.md`)
> **Widgets Nuevos:** `dpg.add_combo` para elegir categoría, resumen en vivo que se
> refresca con cada gasto.

## Punto de partida

El archivo `ejercicio05_control_gastos.py` ya trae la **ventana inicial armada**:
los widgets, sus tags (`combo_categoria`, `input_monto`, `input_descripcion`,
`panel_resumen`, ...) y los botones conectados a los callbacks. Tu trabajo es completar
el resto:

1. Crear el módulo `modulos/servicio_gastos.py` con la lógica que describe el enunciado
   (presupuestos, validación, excesos, resumen) y las funciones de la "Pista".
   Ojo: el combo usa `default_value="comida"` y sus opciones fijas; el presupuesto real
   lo define tu módulo.
2. Completar los callbacks en `ejercicio05_control_gastos.py` para que lean la interfaz
   con `dpg.get_value(...)`, llamen al módulo y actualicen los widgets con
   `dpg.set_value(...)`.

Al ejecutar el archivo, la ventana abre sin errores pero el botón **todavía no hace nada**:
se activa cuando implementes la lógica y los callbacks. La versión resuelta queda guardada
en la carpeta `resuelta/` como referencia.

## La situación

En el Ejercicio 4 de la carpeta anterior armaste un control de gastos por consola: cada
categoría tiene un presupuesto y el programa registra gastos y avisa si te pasás. Ahora
el Android/iOS no va, así que querés la misma herramienta **en una ventana** para usarla
rápido y ver el presupuesto sin leer tablas en la terminal.

## Lo que necesito que haga el programa

1. Un **combo** (`add_combo`) para elegir la **categoría** del gasto, cargada con las
   categorías del presupuesto definido en el código (`comida`, `transporte`, `ocio`).
2. Campos de texto para el **monto** y una **descripción breve**.
3. Botón **Registrar gasto**: valida el monto (número, mayor a cero) y la descripción,
   y lo agrega. Si con ese gasto se **supera el presupuesto** de la categoría, avisa en
   el momento cuánto se pasó.
4. Un **panel de resumen en vivo** que muestre, por cada categoría: presupuesto, gastado
   y lo que queda (puede ser negativo si te pasaste), el total del mes y la lista de
   categorías **superadas**.
5. Un **texto de estado** con el resultado de la última acción.

## Detalles importantes

- El combo **reemplaza al tecleado de la categoría**: al ser los datos ya conocidos, no
  hace falta validar si la categoría existe (aunque el módulo igual lo controla).
- El monto llega como texto: acepta `,` o `.` como separador decimal y rechaza valores
  no numéricos o `<= 0` sin romperse.
- El resumen general se **redibuja después de cada registro exitoso** usando la misma
  técnica de borrar hijos con `dpg.delete_item(...)` y volver a agregar el texto.
- La lógica (presupuestos, validación, excesos, resumen) vive entera en
  `modulos/servicio_gastos.py`.

## Pista de qué conceptos entran en juego

Un diccionario para los presupuestos, una lista de tuplas para los gastos,
`sum()` con `for` como línea de comprensión para totales, `try/except` para el monto,
f-strings con formato `:,.2f` para pesos, y la separación entre el módulo de lógica
(`modulos/servicio_gastos.py`) y la ventana.

## Cómo ejecutarlo

Desde la carpeta de este ejercicio:

```bash
python ejercicio05_control_gastos.py
```