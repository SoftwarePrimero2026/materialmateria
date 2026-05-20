# TP 8 — Torneo deportivo

**Estructuras:** tuplas · listas · diccionarios · funciones  
**Entrada de datos:** sí (`input`)

## Enunciado

El usuario ingresa los resultados de los partidos de un torneo de fútbol. Cada partido se almacena como una tupla `(equipo_local, equipo_visitante, goles_local, goles_visitante)` en una lista. Al finalizar, el programa construye y muestra la tabla de posiciones ordenada.

## Ejemplo de salida esperada

```
============= TABLA DE POSICIONES =============
Pos  Equipo         PJ  G  E  P  GF  GC  Dif  Pts
---------------------------------------------------
 1   River Plate     3  2  1  0   7   3   +4    7
 2   Boca Juniors    3  2  0  1   5   4   +1    6
 3   Racing Club     3  0  1  2   3   6   -3    1
===============================================
```

## Indicaciones

1. Implementar las funciones:
   - `cargar_partidos()` → retorna lista de tuplas
   - `procesar_resultados(partidos)` → retorna diccionario de equipos
   - `ordenar_tabla(estadisticas)` → retorna lista ordenada
   - `mostrar_tabla(tabla_ordenada)` → imprime tabla formateada
2. Cada equipo en el diccionario tiene las claves: `"pj"`, `"g"`, `"e"`, `"p"`, `"gf"`, `"gc"`, `"pts"`.
3. Criterio de orden: primero por `pts` (desc), luego por diferencia de goles `gf - gc` (desc).
4. Usar `"+"` para diferencia positiva y `"-"` para negativa.

## Estructuras sugeridas

```python
partidos = [
    ("River Plate", "Boca Juniors", 2, 1),
    ...
]
estadisticas = {
    "River Plate": {"pj": 0, "g": 0, "e": 0, "p": 0, "gf": 0, "gc": 0, "pts": 0},
    ...
}
```
