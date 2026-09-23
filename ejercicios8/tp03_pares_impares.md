# TP 03 — Separar un arreglo de 100 números en pares e impares

> Iteración eficiente sobre arreglos e invariantes de propiedades.

> **Punto de partida:** el archivo `tp03_pares_impares.py` (junto a este enunciado) es
> un esqueleto con las funciones sugeridas y el `main()`. Completá la lógica de cada
> función sin cambiar la idea del programa.

## La situación

Tengo un montón de números y quiero organizarlos: separar los **pares** de los
**impares**. El programa debe dejar que cargue una lista de números y, al final,
mostrarme dos listas armadas **dinámicamente**: una con los pares y otra con los
impares, sin que yo tenga que ordenarlos a mano.

## Lo que necesito que haga el programa

1. Permitir cargar **hasta 100 números** por teclado. Puedo ingresar los números uno a
   uno, o todos juntos en una línea separados por espacios o comas.
2. Al terminar la carga, **recorrer la lista** y separar cada número en la lista de
   **pares** o la de **impares**, usando el resto de la división por 2 (`% 2`).
3. Mostrar ambas listas y la **cantidad** de números en cada una.
4. Mostrar cada lista **ordenada de menor a mayor**.
5. Antes de finalizar, **volver a preguntar** si quiero cargar otro conjunto de números
   o salir. Con un nuevo conjunto, la separación se vuelve a hacer desde cero.

## Detalles importantes

- La separación debe ser **dinámica**: no sabemos cuántos números van a ser pares o
  impares hasta que se cargan. Por eso se usan dos listas y `append()`.
- Si el usuario ingresa **texto que no es un número** o un número fuera del rango
  permitido, el programa debe avisar y volver a pedirlo **sin romperse** ni contar ese
  intento.
- **Validá el límite de 100**: al superarlo, avisá y no permitas cargar más.
- Recorré la lista de forma **eficiente**: iterá sobre los elementos directamente
  (`for numero in numeros:`), no con índices salvo que los necesites.
- El 0 se considera **par** (0 % 2 == 0).

## Pista de qué conceptos entran en juego

Listas y `append()`, el operador módulo `%` para decidir par/impar, un ciclo para la
carga con validación, iteración directa sobre la colección (y opcionalmente
`enumerate()`), `sorted()` para ordenar, y pensar el **invariante**: tras cada vuelta,
todo número ya recorrido está en su lista correcta. Todo con funciones limpias (TP 01).