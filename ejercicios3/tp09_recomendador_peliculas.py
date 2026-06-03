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

CATALOGO = {
    "Interstellar": {"genero": "Ciencia Ficción", "puntaje": 9.3, "año": 2014},
    "Mad Max: Fury Road": {"genero": "Acción", "puntaje": 8.1, "año": 2015},
    "Gravity": {"genero": "Ciencia Ficción", "puntaje": 7.7, "año": 2013},
    "El Padrino": {"genero": "Drama", "puntaje": 9.2, "año": 1972},
    "Toy Story": {"genero": "Animación", "puntaje": 8.3, "año": 1995},
    "Coco": {"genero": "Animación", "puntaje": 8.4, "año": 2017},
    "Gladiador": {"genero": "Acción", "puntaje": 8.5, "año": 2000},
    "La La Land": {"genero": "Musical", "puntaje": 8.0, "año": 2016},
    "El Conjuro": {"genero": "Terror", "puntaje": 7.5, "año": 2013},
    "Relatos Salvajes": {"genero": "Comedia", "puntaje": 8.1, "año": 2014},
}


def pedir_perfil_usuario():
    """Pide nombre, generos favoritos y peliculas vistas."""
    nombre = input("Nombre: ").strip()

    generos_texto = input("Géneros favoritos separados por coma: ")
    generos = set()
    for genero in generos_texto.split(","):
        generos.add(genero.strip().lower())

    vistas = set()
    print("Peliculas vistas (dejá vacío para terminar):")
    while True:
        titulo = input("Título: ").strip()
        if titulo == "":
            break
        vistas.add(titulo.lower())

    return nombre, generos, vistas


def recomendar(catalogo, generos, vistas):
    """Filtra peliculas no vistas que coinciden con los generos favoritos."""
    recomendaciones = []

    for titulo, datos in catalogo.items():
        genero_normalizado = datos["genero"].lower()
        titulo_normalizado = titulo.lower()

        if genero_normalizado in generos and titulo_normalizado not in vistas:
            recomendaciones.append((titulo, datos["genero"], datos["año"], datos["puntaje"]))

    recomendaciones.sort(key=lambda pelicula: pelicula[3], reverse=True)
    return recomendaciones


def mostrar_recomendaciones(nombre, generos, recomendaciones):
    """Imprime la lista de recomendaciones ordenadas."""
    print(f"\n====== RECOMENDACIONES PARA {nombre.upper()} ======")
    generos_texto = ", ".join(sorted(generos))
    print(f"Géneros favoritos: {generos_texto}")

    if not recomendaciones:
        print("\nNo se encontraron recomendaciones para ese perfil.")
    else:
        print()
        for numero, pelicula in enumerate(recomendaciones, start=1):
            titulo, genero, año, puntaje = pelicula
            print(f"#{numero:<2} {titulo:<18} ({genero}, {año})  ★ {puntaje:.1f}")

        print(f"\n{len(recomendaciones)} recomendaciones encontradas.")

    print("=========================================")


def main():
    nombre, generos, vistas = pedir_perfil_usuario()
    recomendaciones = recomendar(CATALOGO, generos, vistas)
    mostrar_recomendaciones(nombre, generos, recomendaciones)


if __name__ == "__main__":
    main()
