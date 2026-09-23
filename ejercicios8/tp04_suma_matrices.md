# TP 04 — Suma y manipulación de dos matrices

> Arrays multidimensionales (matrices): listas dentro de listas.

> **Punto de partida:** el archivo `tp04_suma_matrices.py` (junto a este enunciado) es
> un esqueleto con las funciones sugeridas y el `main()`. Completá la lógica de cada
> función sin cambiar la idea del programa.

## La situación

Trabajo con tablas de números (por ejemplo, notas por curso o ventas por producto) y
necesito **sumar dos matrices** del mismo tamaño, elemento por elemento, y también poder
**manipularlas** (recorrerlas, calcular totales, multiplicar por un número). Quiero un
programa que las cargue, las opere y me muestre los resultados de forma clara.

## Lo que necesito que haga el programa

1. **Cargar o definir dos matrices** del mismo tamaño (`n` filas × `m` columnas). Pueden
   estar definidas en el código o cargarse por teclado (filas y columnas).
2. **Sumar las dos matrices**: el resultado es otra matriz donde cada celda es la suma
   de las celdas correspondientes (`resultado[i][j] = a[i][j] + b[i][j]`).
3. **Mostrar las matrices** de forma legible (una fila por línea), incluida la matriz
   resultado.
4. **Manipulaciones adicionales**, a elección (al menos dos):
   - Multiplicar una matriz por un **escalar** (número).
   - Calcular el **promedio** de todos sus elementos.
   - Encontrar el **mayor y el menor** valor de una matriz.
   - Calcular la **suma por fila** y la **suma por columna**.

## Detalles importantes

- **Verificá las dimensiones**: si las dos matrices no tienen el mismo tamaño, el
  programa debe avisar "No se pueden sumar" y **no** intentar la operación.
- Las matrices se construyen con la técnica correcta: `[[0] * m for _ in range(n)]`.
  No uses `[[0] * m] * n` (comparten la misma fila y se corrompen).
- Recordá el orden de acceso: `matriz[fila][columna]`; `len(matriz)` da las filas y
  `len(matriz[0])` las columnas.
- Si se cargan por teclado, validá que filas, columnas y valores sean números positivos
  (con `try/except` para que no se rompa).
- Organizá la solución en **funciones**: `crear_matriz()`, `mostrar_matriz()`,
  `sumar_matrices()`, `multiplicar_por_escalar()`, etc.

## Pista de qué conceptos entran en juego

Listas de listas, bucles anidados (uno por filas, otro por columnas), comprensión de
listas para crear matrices, `len()` para dimensiones, y funciones limpias que reciben la
matriz por parámetro y devuelven el resultado por `return` (sin modificar las originales
por sorpresa).