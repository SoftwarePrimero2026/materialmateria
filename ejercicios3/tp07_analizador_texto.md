# TP 7 — Analizador de texto

**Estructuras:** conjuntos · diccionarios · funciones  
**Entrada de datos:** sí (`input`)

## Enunciado

El usuario ingresa dos textos por teclado. El programa determina la cantidad de palabras únicas en cada texto (usando conjuntos), las 5 palabras más frecuentes (usando diccionarios) y si los dos textos comparten más del 50% de su vocabulario.

## Ejemplo de salida esperada

```
============ ANÁLISIS DE TEXTOS ============
Texto 1: 42 palabras únicas
Top 5:  "que"(5), "de"(4), "la"(3), "en"(2), "es"(2)

Texto 2: 38 palabras únicas
Top 5:  "y"(6), "de"(5), "que"(4), "un"(3), "es"(2)

Vocabulario compartido: 21 palabras (54.0%)
→ Los textos SÍ comparten más del 50% del vocabulario.
============================================
```

## Indicaciones

1. Implementar las funciones:
   - `limpiar_texto(texto)` → retorna lista de palabras (sin puntuación, en minúsculas)
   - `palabras_unicas(palabras)` → retorna un `set`
   - `frecuencias(palabras)` → retorna diccionario `{palabra: count}`
   - `top_n(frec, n)` → retorna las n palabras más frecuentes
   - `porcentaje_compartido(set1, set2)` → retorna float
   - `mostrar_analisis(texto1, texto2)` → imprime el informe completo
2. Para limpiar la puntuación, usar el módulo `string` (`string.punctuation`).
3. El porcentaje se calcula como `|intersección| / |unión| * 100`.

## Módulos útiles

```python
import string
# Ejemplo de limpieza:
# texto.lower().translate(str.maketrans('', '', string.punctuation)).split()
```
