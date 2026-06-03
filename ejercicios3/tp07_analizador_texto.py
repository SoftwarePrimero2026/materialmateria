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

import string


def limpiar_texto(texto):
    """Devuelve palabras en minuscula y sin signos de puntuacion."""
    texto_limpio = texto.lower()

    for signo in string.punctuation:
        texto_limpio = texto_limpio.replace(signo, " ")

    palabras = texto_limpio.split()

    # Ignoramos palabras de una sola letra para mejorar el analisis.
    return [palabra for palabra in palabras if len(palabra) >= 2]


def palabras_unicas(palabras):
    """Convierte la lista de palabras en un conjunto sin repetidos."""
    return set(palabras)


def frecuencias(palabras):
    """Cuenta cuantas veces aparece cada palabra."""
    conteo = {}
    for palabra in palabras:
        if palabra in conteo:
            conteo[palabra] += 1
        else:
            conteo[palabra] = 1
    return conteo


def top_n(frecuencias_palabras, n):
    """Devuelve las n palabras mas repetidas."""
    ordenadas = sorted(frecuencias_palabras.items(), key=lambda dato: dato[1], reverse=True)
    return ordenadas[:n]


def porcentaje_compartido(set1, set2):
    """Calcula el porcentaje compartido sobre la union de vocabularios."""
    union = set1 | set2
    if not union:
        return 0

    compartidas = set1 & set2
    return len(compartidas) * 100 / len(union)


def mostrar_top(top):
    """Arma el texto del top con formato simple."""
    partes = []
    for palabra, cantidad in top:
        partes.append(f'"{palabra}"({cantidad})')
    return ", ".join(partes)


def mostrar_analisis(texto1, texto2):
    palabras1 = limpiar_texto(texto1)
    palabras2 = limpiar_texto(texto2)

    unicas1 = palabras_unicas(palabras1)
    unicas2 = palabras_unicas(palabras2)
    top1 = top_n(frecuencias(palabras1), 5)
    top2 = top_n(frecuencias(palabras2), 5)
    compartidas = unicas1 & unicas2
    porcentaje = porcentaje_compartido(unicas1, unicas2)

    print("\n============ ANÁLISIS DE TEXTOS ============")
    print(f"Texto 1: {len(unicas1)} palabras únicas")
    print(f"Top 5: {mostrar_top(top1)}")

    print(f"\nTexto 2: {len(unicas2)} palabras únicas")
    print(f"Top 5: {mostrar_top(top2)}")

    print(f"\nVocabulario compartido: {len(compartidas)} palabras ({porcentaje:.1f}%)")
    if porcentaje > 50:
        print("Los textos SÍ comparten más del 50% del vocabulario.")
    else:
        print("Los textos NO comparten más del 50% del vocabulario.")
    print("============================================")


def main():
    texto1 = input("Ingresá el texto 1: ")
    texto2 = input("Ingresá el texto 2: ")
    mostrar_analisis(texto1, texto2)


if __name__ == "__main__":
    main()
