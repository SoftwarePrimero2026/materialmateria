# TP 05 — Ventas de N sucursales a lo largo de M años

> Algoritmos de recorrido matricial y evaluación de datos agrupados.

> **Punto de partida:** el archivo `tp05_ventas_sucursales.py` (junto a este enunciado)
> es un esqueleto con las funciones sugeridas y el `main()`. Completá la lógica de cada
> función sin cambiar la idea del programa.

## La situación

Tengo una empresa con **varias sucursales** y quiero analizar las **ventas** de cada una
a lo largo de varios **años**. Los datos forman una tabla: cada fila es una sucursal y
cada columna es un año. Quiero que el programa me ayude a **recorrerla** y sacar
conclusiones: qué sucursal vende mejor en promedio y en qué año se vendió más en total.

## Lo que necesito que haga el programa

1. **Ingresar `N` (cantidad de sucursales) y `M` (cantidad de años)**, y **cargar la
   matriz** de ventas: `ventas[sucursal][año] = monto`.
2. Mostrar la **tabla de ventas** completa (una fila por sucursal).
3. Calcular y mostrar el **promedio de ventas por sucursal** (recorriendo **filas**).
4. Calcular y mostrar el **total de ventas por año** (recorriendo **columnas**).
5. **Buscar los máximos promedios**: mostrar la sucursal (o sucursales) con el **mayor
   promedio** y el **año con el mayor total** de ventas.
6. Mostrar un **resumen final** ordenado: sucursales por promedio de mayor a menor.

## Detalles importantes

- Validá que `N` y `M` sean números enteros **positivos** (mínimo 1) y que los montos
  sean **mayores o iguales a cero**, con `try/except` para no romperse.
- El **recorrido por columnas** es el truco de este TP: para un año fijo `j`, recorrés
  `ventas[i][j]` variando la sucursal `i`. No confundas fila y columna.
- Si **dos sucursales empatan** en el máximo promedio, mostralas a ambas.
- Organizá cada cálculo en una **función**: `cargar_ventas()`, `promedio_por_sucursal()`,
  `total_por_anio()`, `sucursal_max_promedio()`, `mostrar_tabla()`, etc.
- Las funciones deben **recibir la matriz por parámetro** y devolver los resultados por
  `return` (sin usar variables globales).

## Pista de qué conceptos entran en juego

Matrices (listas de listas), bucles anidados, **recorrido por filas y por columnas**,
acumuladores con `sum()`, cálculo de promedios, búsqueda de máximos (`max()` o
comparaciones) y ordenamiento de resultados. Aplicá además funciones limpias y la
validación de entradas de los TP anteriores.