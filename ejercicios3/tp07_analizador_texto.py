# =============================================================================
# TP 7 — Analizador de texto
# =============================================================================
#
# ENUNCIADO:
#   El usuario ingresa dos textos por teclado. El programa analiza el
#   vocabulario de cada uno y los compara.
#
# ESTRUCTURAS A UTILIZAR:
#   - Conjuntos (set) : para las palabras únicas de cada texto.
#   - Diccionario     : para contar la frecuencia de cada palabra.
#   - Funciones       : una por cada operación de análisis.
#
# ENTRADA DE DATOS (input):
#   - El usuario ingresa el texto 1 y el texto 2 (pueden ser párrafos largos).
#
# SALIDA (print formateado):
#   - Resumen de vocabulario y top 5 palabras de cada texto.
#   - Resultado de comparación de vocabulario compartido.
#
# EJEMPLO DE SALIDA ESPERADA:
#   ============ ANÁLISIS DE TEXTOS ============
#   Texto 1: 42 palabras únicas
#   Top 5:  "que"(5), "de"(4), "la"(3), "en"(2), "es"(2)
#
#   Texto 2: 38 palabras únicas
#   Top 5:  "y"(6), "de"(5), "que"(4), "un"(3), "es"(2)
#
#   Vocabulario compartido: 21 palabras (54.0%)
#   → Los textos SÍ comparten más del 50% del vocabulario.
#   ============================================
#
# INDICACIONES:
#   1. Implementar las funciones:
#        - limpiar_texto(texto)           → retorna lista de palabras limpias
#          (sin signos de puntuación, en minúsculas)
#        - palabras_unicas(palabras)      → retorna un conjunto
#        - frecuencias(palabras)          → retorna diccionario {palabra: count}
#        - top_n(frecuencias, n)          → retorna las n palabras más frecuentes
#        - porcentaje_compartido(set1, set2) → retorna float
#        - mostrar_analisis(texto1, texto2)  → imprime el informe completo
#   2. Para limpiar la puntuación, usar el módulo `string` (string.punctuation).
#   3. Ignorar palabras vacías de menos de 2 caracteres es opcional pero sugerido.
#   4. El porcentaje se calcula sobre la unión de ambos vocabularios.
#
# =============================================================================

# Escribí tu código a partir de aquí:
