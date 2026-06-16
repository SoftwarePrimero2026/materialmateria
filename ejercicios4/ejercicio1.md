# Ejercicio 1 — Cajero automático con movimientos

## La situación

Trabajo en un banco y queremos un programa que simule el **cajero automático** para una
cuenta. La persona se identifica con un PIN y, una vez adentro, puede operar con su
dinero. Lo más importante es que el **saldo y el historial de movimientos no se pierdan**
entre una sesión y otra, así que tienen que guardarse en un archivo.

## Lo que necesito que haga el programa

Al iniciar, el programa debe **leer un archivo** (por ejemplo `cuenta.txt`) que contiene
el saldo actual de la cuenta. Si el archivo no existe (primera vez que se usa), debe
arrancar con un saldo de **$0** sin romperse.

Antes de mostrar cualquier opción, el cajero pide el **PIN** (un número de 4 cifras
definido en el código, por ejemplo `1234`). El usuario tiene como máximo **3 intentos**
para ingresarlo bien; si falla las 3 veces, el programa muestra "Tarjeta bloqueada" y
termina.

Una vez identificado, debe mostrar un **menú** que se repita hasta que el usuario elija
salir:

1. **Consultar saldo**: muestra el saldo actual.
2. **Depositar dinero**: pide un monto y lo suma al saldo.
3. **Retirar dinero**: pide un monto y lo resta del saldo, pero solo si hay saldo
   suficiente. Si el monto supera el saldo, debe avisar "Fondos insuficientes" y no hacer
   la operación.
4. **Ver historial de movimientos**: muestra todos los movimientos de la sesión (tipo de
   operación y monto), numerados.
5. **Salir**: antes de cerrar, guarda el saldo actualizado en el archivo.

## Detalles importantes

- Cada depósito o retiro debe registrarse en el **historial** (por ejemplo, guardando una
  tupla `("Depósito", 5000)` en una lista) para poder mostrarlo después.
- Los montos deben ser números **mayores a cero**. Si el usuario ingresa texto o un
  número inválido (negativo o cero), el programa debe avisar y volver a pedir el dato,
  sin romperse.
- En los retiros, además, podés exigir que el monto sea **múltiplo de 100** (como un
  cajero real que solo entrega ciertos billetes). Si no lo es, avisar y volver a pedir.
- Si elijo una opción del menú que no existe, el programa debe avisar y volver a mostrar
  el menú.

## Pista de qué conceptos entran en juego

Lectura y escritura de archivos (cargar el saldo al inicio y guardarlo al salir), un ciclo
para el control de intentos del PIN, otro ciclo para el menú, decisiones para validar
fondos y opciones, una lista de tuplas para el historial, y manejo de errores con
`try/except` para los montos mal ingresados.
