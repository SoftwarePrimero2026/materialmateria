# TP 4 — Registro de temperaturas semanales

**Estructuras:** tuplas · listas · funciones  
**Entrada de datos:** sí (`input`)

## Enunciado

El usuario ingresa las temperaturas máxima y mínima de cada día de la semana. Cada día se almacena como una tupla `(día, temp_max, temp_min)` en una lista. El programa calcula estadísticas y las presenta en una tabla.

## Ejemplo de salida esperada

```
======= RESUMEN SEMANAL DE TEMPERATURAS =======
Día           Máx     Mín     Amplitud
-----------------------------------------------
Lunes         28°C    15°C    13°C
Martes        31°C    18°C    13°C
Miércoles     25°C    12°C    13°C  ← mayor amplitud
...

Promedios:  Máx 27.4°C  |  Mín 14.8°C
Día más caluroso:  Martes (31°C)
Día más frío:      Miércoles (12°C)
Días con amplitud > 12°C: Lunes, Martes, Miércoles
===============================================
```

## Indicaciones

1. Definir la lista de días de la semana en el código.
2. Implementar las funciones:
   - `cargar_temperaturas()` → retorna lista de tuplas
   - `promedio_maximas(registros)` → retorna float
   - `promedio_minimas(registros)` → retorna float
   - `dia_mas_caluroso(registros)` → retorna la tupla del día más caluroso
   - `dia_mas_frio(registros)` → retorna la tupla del día más frío
   - `dias_alta_amplitud(registros, umbral)` → retorna lista de días
   - `mostrar_tabla(registros)` → imprime la tabla formateada
3. Validar que `temp_max >= temp_min` al ingresar datos.
4. Marcar con `← mayor amplitud` la fila correspondiente en la tabla.

## Estructuras sugeridas

```python
registros = []   # [ ("Lunes", 28, 15), ("Martes", 31, 18), ... ]
```
