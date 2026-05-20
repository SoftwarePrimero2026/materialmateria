# TP 3 — Comparador de materias cursadas

**Estructuras:** conjuntos · listas · funciones  
**Entrada de datos:** no (datos definidos en el código)

## Enunciado

Dados dos alumnos con sus materias aprobadas (almacenadas como conjuntos) y una lista general de materias de la carrera, crear funciones que calculen y muestren:

- Materias aprobadas por ambos alumnos.
- Materias que solo aprobó el alumno A.
- Materias que solo aprobó el alumno B.
- Materias que ninguno aprobó todavía.

La salida debe mostrar claramente cada sección con encabezados y los resultados ordenados alfabéticamente.

## Ejemplo de salida esperada

```
======= COMPARADOR DE MATERIAS =======
Alumno A: Lucía Torres
Alumno B: Martín López

✔ Aprobaron ambos (2):
   · Matemática I
   · Programación I

→ Solo aprobó Lucía (1):
   · Física I

→ Solo aprobó Martín (1):
   · Química

✘ Ninguno aprobó aún (2):
   · Redes
   · Sistemas Operativos
======================================
```

## Indicaciones

1. Definir en el código una lista `materias_carrera` con al menos 8 materias, y dos conjuntos `aprobadas_a` y `aprobadas_b`.
2. Implementar las funciones:
   - `aprobaron_ambos(a, b)` → intersección (`&`)
   - `solo_aprobo(a, b)` → diferencia (`a - b`)
   - `ninguno_aprobo(a, b, carrera)` → `set(carrera) - (a | b)`
   - `mostrar_comparacion(...)` → imprime el informe completo
3. Usar operaciones de conjuntos (`&`, `|`, `-`) directamente, sin loops manuales.
4. Ordenar todos los resultados alfabéticamente antes de imprimir.

## Estructuras sugeridas

```python
materias_carrera = ["Matemática I", "Física I", ...]  # lista
aprobadas_a      = {"Matemática I", "Programación I", ...}  # set
aprobadas_b      = {"Matemática I", "Química", ...}         # set
```
