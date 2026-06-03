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


def aprobaron_ambos(a, b):
    """Devuelve las materias que estan en ambos conjuntos."""
    return a & b


def solo_aprobó(a, b):
    """Devuelve las materias que aprobo el primer alumno y el segundo no."""
    return a - b


def ninguno_aprobó(a, b, carrera):
    """Devuelve materias de la carrera que no aprobo ningun alumno."""
    return set(carrera) - (a | b)


def imprimir_lista(materias):
    """Imprime una lista ordenada de materias."""
    for materia in sorted(materias):
        print(f"   · {materia}")


def mostrar_comparacion(nombre_a, nombre_b, aprobadas_a, aprobadas_b, materias_carrera):
    compartidas = aprobaron_ambos(aprobadas_a, aprobadas_b)
    solo_a = solo_aprobó(aprobadas_a, aprobadas_b)
    solo_b = solo_aprobó(aprobadas_b, aprobadas_a)
    ninguna = ninguno_aprobó(aprobadas_a, aprobadas_b, materias_carrera)

    print("======= COMPARADOR DE MATERIAS =======")
    print(f"Alumno A: {nombre_a}")
    print(f"Alumno B: {nombre_b}")

    print(f"\nAprobaron ambos ({len(compartidas)}):")
    imprimir_lista(compartidas)

    print(f"\nSolo aprobo {nombre_a} ({len(solo_a)}):")
    imprimir_lista(solo_a)

    print(f"\nSolo aprobo {nombre_b} ({len(solo_b)}):")
    imprimir_lista(solo_b)

    print(f"\nNinguno aprobo aun ({len(ninguna)}):")
    imprimir_lista(ninguna)
    print("======================================")


def main():
    materias_carrera = [
        "Matemática I",
        "Programación I",
        "Física I",
        "Química",
        "Sistemas Operativos",
        "Redes",
        "Base de Datos",
        "Inglés Técnico",
    ]

    aprobadas_a = {"Matemática I", "Programación I", "Física I", "Base de Datos"}
    aprobadas_b = {"Matemática I", "Programación I", "Química", "Inglés Técnico"}

    mostrar_comparacion("Lucía Torres", "Martín López", aprobadas_a, aprobadas_b, materias_carrera)


if __name__ == "__main__":
    main()
