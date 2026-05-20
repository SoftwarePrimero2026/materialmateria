# =============================================================================
# TP 4 — Registro de temperaturas semanales
# =============================================================================
#
# ENUNCIADO:
#   El usuario ingresa las temperaturas máxima y mínima de cada día de la
#   semana. El programa almacena los datos y calcula estadísticas.
#
# ESTRUCTURAS A UTILIZAR:
#   - Lista  : para almacenar las tuplas de cada día.
#   - Tuplas : cada elemento de la lista es (día, temp_max, temp_min).
#   - Funciones : una por cada cálculo estadístico.
#
# ENTRADA DE DATOS (input):
#   - Para cada uno de los 7 días, el usuario ingresa temp_max y temp_min.
#   - El usuario también ingresa el umbral de amplitud térmica a consultar.
#
# SALIDA (print formateado):
#   - Tabla semanal con columnas alineadas.
#   - Resumen de promedios, día más caluroso, más frío y días con alta amplitud.
#
# EJEMPLO DE SALIDA ESPERADA:
#   ======= RESUMEN SEMANAL DE TEMPERATURAS =======
#   Día           Máx     Mín     Amplitud
#   -----------------------------------------------
#   Lunes         28°C    15°C    13°C
#   Martes        31°C    18°C    13°C
#   Miércoles     25°C    12°C    13°C  ← mayor amplitud
#   ...
#   Promedios:  Máx 27.4°C  |  Mín 14.8°C
#   Día más caluroso:  Martes (31°C)
#   Día más frío:      Miércoles (12°C)
#   Días con amplitud > 12°C: Lunes, Martes, Miércoles
#   ===============================================
#
# INDICACIONES:
#   1. Definir la lista de días de la semana en el código.
#   2. Implementar las funciones:
#        - cargar_temperaturas()           → retorna lista de tuplas
#        - promedio_maximas(registros)     → retorna float
#        - promedio_minimas(registros)     → retorna float
#        - dia_mas_caluroso(registros)     → retorna tupla del día más caluroso
#        - dia_mas_frio(registros)         → retorna tupla del día más frío
#        - dias_alta_amplitud(registros, umbral) → retorna lista de días
#        - mostrar_tabla(registros)        → imprime la tabla formateada
#   3. Validar que temp_max >= temp_min al cargar datos.
#   4. Marcar con "← mayor amplitud" la fila correspondiente en la tabla.
#
# =============================================================================

# Escribí tu código a partir de aquí:
