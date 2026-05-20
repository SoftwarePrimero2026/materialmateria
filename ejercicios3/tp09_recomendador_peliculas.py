# =============================================================================
# TP 9 — Recomendador de películas
# =============================================================================
#
# ENUNCIADO:
#   Un catálogo de películas está definido en el código. El usuario ingresa
#   sus géneros favoritos y los títulos que ya vio. El programa recomienda
#   películas que no vio y que coincidan con sus intereses.
#
# ESTRUCTURAS A UTILIZAR:
#   - Diccionario  : catálogo de películas con sus atributos.
#   - Conjuntos    : géneros favoritos del usuario y películas vistas.
#   - Lista        : lista de recomendaciones ordenadas por puntaje.
#   - Funciones    : una por cada parte del flujo.
#
# ENTRADA DE DATOS (input):
#   - El nombre del usuario.
#   - Sus géneros favoritos (separados por coma).
#   - Los títulos de películas que ya vio (una por línea hasta dejar vacío).
#
# SALIDA (print formateado):
#   - Lista de recomendaciones numeradas, con género, año y puntaje.
#
# EJEMPLO DE SALIDA ESPERADA:
#   ====== RECOMENDACIONES PARA JORGE ======
#   Géneros favoritos: Acción, Ciencia Ficción
#
#   #1  Interstellar        (Ciencia Ficción, 2014)  ★ 9.3
#   #2  Mad Max: Fury Road  (Acción, 2015)           ★ 8.1
#   #3  Gravity             (Ciencia Ficción, 2013)  ★ 7.7
#
#   3 recomendaciones encontradas.
#   =========================================
#
# INDICACIONES:
#   1. Definir en el código un catálogo con al menos 10 películas.
#      Formato sugerido: { "Título": {"genero": "...", "puntaje": X.X, "año": XXXX} }
#   2. Implementar las funciones:
#        - pedir_perfil_usuario()          → retorna (nombre, generos_set, vistas_set)
#        - recomendar(catalogo, generos, vistas) → retorna lista de tuplas ordenadas
#        - mostrar_recomendaciones(nombre, generos, recomendaciones)
#   3. La comparación de géneros debe ser insensible a mayúsculas.
#   4. Si no hay recomendaciones, mostrar un mensaje adecuado.
#   5. Ordenar por puntaje de mayor a menor.
#
# =============================================================================

# Escribí tu código a partir de aquí:
