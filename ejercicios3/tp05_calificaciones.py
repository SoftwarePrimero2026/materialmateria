# =============================================================================
# TP 5 — Sistema de calificaciones escolares
# =============================================================================
#
# ENUNCIADO:
#   Crear un sistema donde el usuario carga alumnos con sus notas. El programa
#   calcula promedios, genera un ranking y detecta alumnos en riesgo.
#
# ESTRUCTURAS A UTILIZAR:
#   - Diccionario : clave = nombre del alumno, valor = lista de notas.
#   - Lista       : almacena las notas de cada alumno.
#   - Funciones   : una por cada operación.
#
# ENTRADA DE DATOS (input):
#   - El usuario ingresa el nombre del alumno y luego sus notas (separadas
#     por coma o de a una hasta ingresar una señal de fin).
#
# SALIDA (print formateado):
#   - Tabla con ranking, nombre, notas y promedio.
#   - Sección especial con alumnos en riesgo (promedio < 6).
#
# EJEMPLO DE SALIDA ESPERADA:
#   ======= SISTEMA DE CALIFICACIONES =======
#   #   Alumno              Notas            Promedio
#   -------------------------------------------------
#   1   Valentina Ruiz      [8, 9, 7, 10]    8.50  ✔
#   2   Bruno Sosa          [6, 5, 7, 6]     6.00  ✔
#   3   Camila Díaz         [4, 5, 3, 6]     4.50  ✘
#
#   ⚠ En riesgo de desaprobar:
#     · Camila Díaz (promedio: 4.50)
#   =========================================
#
# INDICACIONES:
#   1. Implementar las funciones:
#        - agregar_alumno(calificaciones)     → pide nombre y notas, las guarda
#        - calcular_promedio(notas)           → retorna el promedio como float
#        - mostrar_ranking(calificaciones)    → ordena por promedio e imprime tabla
#        - alumnos_en_riesgo(calificaciones)  → retorna lista de alumnos con prom < 6
#   2. Las notas deben ser números entre 1 y 10; validar el rango.
#   3. Mostrar ✔ o ✘ según apruebe o no (promedio >= 6).
#   4. El ranking se ordena de mayor a menor promedio.
#
# =============================================================================

# Escribí tu código a partir de aquí:
