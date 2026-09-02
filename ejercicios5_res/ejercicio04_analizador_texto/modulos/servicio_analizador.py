"""Lógica del analizador de texto, separada de la interfaz.

Basada en el TP 7: limpieza de texto, vocabulario con conjuntos y
frecuencias con diccionarios. Acá se analiza un único texto y se arma
un informe completo como cadena para mostrar en la ventana.
"""

import string


def limpiar_texto(texto):
    """Devuelve la lista de palabras, en minúsculas y sin puntuación."""
    texto_limpio = texto.lower().translate(str.maketrans("", "", string.punctuation))
    return texto_limpio.split()


def frecuencias(palabras):
    """Devuelve un diccionario {palabra: cantidad_de_apariciones}."""
    frecuencia = {}
    for palabra in palabras:
        frecuencia[palabra] = frecuencia.get(palabra, 0) + 1
    return frecuencia


def top_n(palabras, n=5):
    """Devuelve las n palabras más frecuentes, de mayor a menor."""
    frecuencia = frecuencias(palabras)
    ordenadas = sorted(frecuencia.items(), key=lambda par: (-par[1], par[0]))
    return ordenadas[:n]


def analizar_texto(texto):
    """Arma el informe del análisis como una cadena lista para la GUI."""
    palabras = limpiar_texto(texto)

    if not palabras:
        return "El texto no tiene palabras para analizar."

    total = len(palabras)
    unicas = set(palabras)
    top = top_n(palabras)
    palabra_mas_larga = max(palabras, key=len)
    largo_promedio = sum(len(palabra) for palabra in palabras) / total

    informe = "============ ANÁLISIS DE TEXTO ============\n"
    informe += f"Palabras totales: {total}\n"
    informe += f"Palabras únicas: {len(unicas)}\n"
    informe += f"Palabra más larga: '{palabra_mas_larga}' ({len(palabra_mas_larga)} letras)\n"
    informe += f"Largo promedio por palabra: {largo_promedio:.2f} letras\n"
    informe += "\nTop 5 palabras más frecuentes:\n"

    for palabra, cantidad in top:
        informe += f"  {palabra:<18} {cantidad:>3} vez/veces\n"

    informe += "=" * 37
    return informe