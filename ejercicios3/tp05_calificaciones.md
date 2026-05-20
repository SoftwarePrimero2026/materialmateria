# TP 5 — Sistema de calificaciones escolares

**Estructuras:** diccionarios · listas · funciones  
**Entrada de datos:** sí (`input`)

## Enunciado

Crear un sistema donde el usuario ingresa alumnos y sus notas. Cada alumno es una clave en el diccionario y su valor es una lista de notas numéricas. El programa calcula promedios, genera un ranking y alerta sobre alumnos en riesgo de desaprobar.

## Ejemplo de salida esperada

```
======= SISTEMA DE CALIFICACIONES =======
#   Alumno              Notas            Promedio
-------------------------------------------------
1   Valentina Ruiz      [8, 9, 7, 10]    8.50  ✔
2   Bruno Sosa          [6, 5, 7, 6]     6.00  ✔
3   Camila Díaz         [4, 5, 3, 6]     4.50  ✘

⚠ En riesgo de desaprobar:
  · Camila Díaz (promedio: 4.50)
=========================================
```

## Indicaciones

1. Implementar las funciones:
   - `agregar_alumno(calificaciones)` → pide nombre y notas, los guarda
   - `calcular_promedio(notas)` → retorna el promedio como float
   - `mostrar_ranking(calificaciones)` → ordena por promedio e imprime tabla
   - `alumnos_en_riesgo(calificaciones)` → retorna lista de alumnos con promedio < 6
2. Las notas deben ser números entre 1 y 10; validar el rango.
3. Mostrar `✔` si el promedio es >= 6, `✘` si es menor.
4. El ranking se ordena de mayor a menor promedio.

## Estructuras sugeridas

```python
calificaciones = {}  # { "Valentina Ruiz": [8, 9, 7, 10], ... }
```
