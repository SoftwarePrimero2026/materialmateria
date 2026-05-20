# =============================================================================
# TP 3 — Comparador de materias cursadas
# =============================================================================
#
# ENUNCIADO:
#   Dados dos alumnos con sus materias aprobadas (almacenadas como conjuntos)
#   y una lista general de materias de la carrera, mostrar qué materias
#   aprobó cada uno, cuáles comparten y cuáles no aprobó ninguno.
#
# ESTRUCTURAS A UTILIZAR:
#   - Conjuntos (set) : para las materias aprobadas de cada alumno.
#   - Lista           : para la lista general de materias de la carrera.
#   - Funciones       : una función por cada tipo de comparación.
#
# ENTRADA DE DATOS (input):
#   - Los datos de alumnos y materias se definen directamente en el código
#     (no se requiere input en este ejercicio).
#
# SALIDA (print formateado):
#   - Mostrar cada sección con encabezado propio y los resultados ordenados
#     alfabéticamente.
#
# EJEMPLO DE SALIDA ESPERADA:
#   ======= COMPARADOR DE MATERIAS =======
#   Alumno A: Lucía Torres
#   Alumno B: Martín López
#
#   ✔ Aprobaron ambos (2):
#      · Matemática I
#      · Programación I
#
#   → Solo aprobó Lucía (1):
#      · Física I
#
#   → Solo aprobó Martín (1):
#      · Química
#
#   ✘ Ninguno aprobó aún (2):
#      · Redes
#      · Sistemas Operativos
#   ======================================
#
# INDICACIONES:
#   1. Definir los siguientes conjuntos y lista en el código:
#        materias_carrera = [...]   (al menos 8 materias)
#        aprobadas_a      = {...}
#        aprobadas_b      = {...}
#   2. Implementar las funciones:
#        - aprobaron_ambos(a, b)          → intersección
#        - solo_aprobó(a, b)              → diferencia a - b
#        - ninguno_aprobó(a, b, carrera)  → carrera - (a ∪ b)
#        - mostrar_comparacion(...)       → imprime el informe completo
#   3. Usar operaciones de conjuntos (&, |, -, ^) directamente.
#   4. Ordenar todos los resultados alfabéticamente antes de imprimir.
#
# =============================================================================

# Escribí tu código a partir de aquí:
