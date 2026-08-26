# Ejercicio 5 — Control de gastos con historial guardado

> **Migración de:** Ejercicio 4 — Control de gastos personales
> (`../../ejercicios4/ejercicio4.md`)
> **Conceptos nuevos:** el historial de gastos se **lee al iniciar** y se **guarda al
> salir**; el programa "recuerda" lo cargado en la sesión anterior.

## Punto de partida

El archivo `ejercicio05_control_gastos.py` ya trae la **ventana inicial armada**: los
widgets, sus tags (`combo_categoria`, `input_monto`, `input_descripcion`,
`panel_resumen`, `txt_estado`, ...) y los botones conectados a los callbacks. Tu
trabajo es completar el resto:

1. Crear el módulo `modulos/servicio_gastos.py` con la lógica que describe el enunciado
   (presupuestos, carga del archivo, validación, excesos, resumen, guardado) y las
   funciones de la "Pista".
2. Completar los callbacks en `ejercicio05_control_gastos.py` para que lean la interfaz
   con `dpg.get_value(...)`, llamen al módulo y actualicen los widgets con
   `dpg.set_value(...)`.

Al ejecutar el archivo, la ventana abre sin errores pero el botón **todavía no hace
nada**: se activa cuando implementes la lógica y los callbacks.

## La situación

Quiero ordenar mis finanzas. Tengo un presupuesto fijo por categoría (comida,
transporte y ocio) y necesito ir **anotando mis gastos** del mes desde una ventana,
que el programa me **avise cuando me paso** del presupuesto, y que todo el historial
**quede guardado**: la próxima vez que abra el programa quiero ver los gastos que ya
cargué, sin tener que anotarlos de nuevo.

## Lo que necesito que haga el programa

1. Un **combo** (`add_combo`) para elegir la **categoría** del gasto, cargada con las
   categorías del presupuesto definido en el código (`comida`, `transporte`, `ocio`).
2. Campos de texto para el **monto** y una **descripción breve**.
3. Botón **Registrar gasto**: valida el monto (número, mayor a cero) y la descripción,
   y lo agrega. Si con ese gasto se **supera el presupuesto** de la categoría, avisa en
   el momento cuánto te pasaste.
4. Un **panel de resumen en vivo** que muestre, por cada categoría: presupuesto, gastado
   y lo que queda (puede ser negativo si te pasaste), el **total del mes** y la lista de
   categorías **superadas**. El panel se actualiza después de cada registro.
5. Botón **Guardar**: escribe todos los gastos en `gastos.txt`.
6. Al **iniciar**, el programa lee `gastos.txt` y carga los gastos ya guardados. Si el
   archivo no existe, arranca sin gastos, sin romperse.
7. Un **texto de estado** con el resultado de la última acción.

## Detalles importantes

- El **archivo** tiene una línea por gasto con el formato `categoria;monto;descripcion`,
  por ejemplo `transporte;1200;subte`. La carga y el guardado se hacen **en el módulo**
  de lógica, nunca en la ventana.
- El **monto llega como texto**: aceptá `,` o `.` como separador decimal y rechazá
  valores no numéricos o `<= 0` sin romperte.
- Solo se aceptan categorías que **existan** en el presupuesto definido (el combo ya las
  trae, pero el módulo igual lo controla).
- "Cuánto me queda" puede dar negativo si te pasaste: en ese caso mostralo como un
  sobregiro/exceso.
- El resumen general se **redibuja después de cada registro exitoso** usando la misma
  técnica de borrar hijos con `dpg.delete_item(...)` y volver a agregar el texto.

## Pista de qué conceptos entran en juego

Un diccionario para los **presupuestos**, una lista de tuplas para los **gastos** que
se carga del archivo al iniciar, `sum()` con `for` como línea de comprensión para los
totales, `try/except` para el monto, `open(..., "r")` / `open(..., "w")` con `with` y
`split(";")` para el historial, f-strings con formato `:,.2f` para pesos, y la
separación entre el módulo de lógica (`modulos/servicio_gastos.py`) y la ventana.

## Cómo ejecutarlo

Desde la carpeta de este ejercicio:

```bash
python ejercicio05_control_gastos.py
```