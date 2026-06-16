# Ejercicio 4 — Control de gastos personales

## La situación

Quiero ordenar mis finanzas. Necesito un programa donde pueda ir **anotando mis gastos**
del mes, clasificándolos por categoría (comida, transporte, ocio, etc.), y que me avise
cuando me estoy pasando del presupuesto que me fijé para cada categoría. Y que todo quede
**guardado** para no volver a cargarlo cada vez.

## Lo que necesito que haga el programa

En el código se define un **presupuesto por categoría**, por ejemplo:
comida $50.000, transporte $20.000, ocio $15.000.

Al iniciar, el programa debe **leer un archivo** (por ejemplo `gastos.txt`) con los gastos
ya cargados. Si el archivo no existe todavía, arranca sin gastos, sin romperse.

Luego muestra un **menú** que se repite hasta salir:

1. **Registrar un gasto**: pide la **categoría**, el **monto** y una breve **descripción**
   (por ejemplo: "transporte, 1200, subte"). El gasto se agrega a la lista de gastos.
2. **Ver gastos por categoría**: me pide una categoría y muestra todos los gastos de esa
   categoría con su descripción y monto, más el **total gastado** y **cuánto me queda**
   del presupuesto de esa categoría.
3. **Ver resumen general**, que muestre:
   - El **total gastado** en el mes (todas las categorías).
   - El total gastado **por cada categoría**.
   - En qué categorías **me pasé del presupuesto** (y por cuánto).
   - La categoría en la que **más gasté**.
4. **Salir**: guarda todos los gastos en el archivo.

## Detalles importantes

- Solo se aceptan categorías que **existan** en el presupuesto definido. Si ingreso una
  categoría que no está, el programa debe avisar y no registrar el gasto.
- El monto debe ser un número **mayor a cero**. Si ingreso texto o un valor inválido, el
  programa debe avisar y volver a pedirlo, sin romperse.
- Cada vez que registro un gasto, si con ese gasto **supero el presupuesto** de la
  categoría, el programa debe avisarme en el momento (por ejemplo: "¡Atención! Te pasaste
  del presupuesto de ocio").
- "Cuánto me queda" puede dar negativo si me pasé: en ese caso, mostralo como un
  sobregiro/exceso.

## Pista de qué conceptos entran en juego

Lectura y escritura de archivos, un diccionario para los presupuestos por categoría, una
lista (de tuplas o diccionarios) para los gastos, un ciclo para el menú, recorridos y
acumuladores para sumar por categoría, decisiones para las alertas de presupuesto,
funciones para organizar cada cálculo y manejo de errores para los montos y categorías
inválidas.
