# =============================================================================
# TP 8 — Torneo deportivo
# =============================================================================
#
# ENUNCIADO:
#   El usuario carga los resultados de los partidos de un torneo de fútbol.
#   El programa construye y muestra la tabla de posiciones completa.
#
# ESTRUCTURAS A UTILIZAR:
#   - Lista       : para almacenar los resultados (una tupla por partido).
#   - Tuplas      : cada partido es (equipo_local, equipo_visitante, goles_l, goles_v).
#   - Diccionario : para acumular estadísticas por equipo.
#   - Funciones   : una por cada parte del procesamiento.
#
# ENTRADA DE DATOS (input):
#   - El usuario ingresa los datos de cada partido.
#   - El sistema pregunta si desea cargar otro partido hasta que el usuario indique fin.
#
# SALIDA (print formateado):
#   - Tabla de posiciones ordenada por puntos (y diferencia de goles como desempate).
#
# EJEMPLO DE SALIDA ESPERADA:
#   ============= TABLA DE POSICIONES =============
#   Pos  Equipo         PJ  G  E  P  GF  GC  Dif  Pts
#   ---------------------------------------------------
#    1   River Plate     3  2  1  0   7   3   +4    7
#    2   Boca Juniors    3  2  0  1   5   4   +1    6
#    3   Racing Club     3  0  1  2   3   6   -3    1
#   ===============================================
#
# INDICACIONES:
#   1. Implementar las funciones:
#        - cargar_partidos()                      → retorna lista de tuplas
#        - procesar_resultados(partidos)          → retorna diccionario de equipos
#        - ordenar_tabla(estadisticas)            → retorna lista ordenada
#        - mostrar_tabla(tabla_ordenada)          → imprime tabla formateada
#   2. Cada equipo en el diccionario tiene las claves:
#        "pj", "g", "e", "p", "gf", "gc", "pts"
#   3. Criterio de ordenamiento: primero por pts (desc), luego por (gf-gc) (desc).
#   4. Prefijo "+" para diferencia positiva, "-" para negativa.
#   5. Si un equipo aparece solo como visitante en todos sus partidos,
#      igual debe estar registrado en la tabla.
#
# =============================================================================

# Escribí tu código a partir de aquí:
