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


def pedir_nota():
    """Pide una nota y valida que este entre 1 y 10."""
    while True:
        nota = float(input("Nota (1 a 10): "))
        if 1 <= nota <= 10:
            return nota
        print("La nota debe estar entre 1 y 10.")


def agregar_alumno(calificaciones):
    """Pide nombre y notas, y las guarda en el diccionario."""
    nombre = input("Nombre del alumno: ").strip()

    if nombre in calificaciones:
        print("Ese alumno ya esta cargado.")
        return

    notas = []
    cantidad = int(input("Cuantas notas querés cargar?: "))

    for numero in range(cantidad):
        print(f"Nota {numero + 1}:")
        notas.append(pedir_nota())

    calificaciones[nombre] = notas
    print("Alumno agregado correctamente.")


def calcular_promedio(notas):
    """Calcula el promedio de una lista de notas."""
    return sum(notas) / len(notas)


def alumnos_en_riesgo(calificaciones):
    """Devuelve alumnos cuyo promedio es menor a 6."""
    riesgo = []
    for alumno, notas in calificaciones.items():
        promedio = calcular_promedio(notas)
        if promedio < 6:
            riesgo.append((alumno, promedio))
    return riesgo


def mostrar_ranking(calificaciones):
    """Ordena por promedio y muestra una tabla."""
    if not calificaciones:
        print("No hay alumnos cargados.")
        return

    ranking = []
    for alumno, notas in calificaciones.items():
        ranking.append((alumno, notas, calcular_promedio(notas)))

    ranking.sort(key=lambda dato: dato[2], reverse=True)

    print("\n======= SISTEMA DE CALIFICACIONES =======")
    print(f"{'#':<4}{'Alumno':<20}{'Notas':<18}{'Promedio'}")
    print("-------------------------------------------------")

    for posicion, dato in enumerate(ranking, start=1):
        alumno, notas, promedio = dato
        estado = "✔" if promedio >= 6 else "✘"
        print(f"{posicion:<4}{alumno:<20}{str(notas):<18}{promedio:.2f}  {estado}")

    riesgo = alumnos_en_riesgo(calificaciones)
    print("\nEn riesgo de desaprobar:")
    if riesgo:
        for alumno, promedio in riesgo:
            print(f"  · {alumno} (promedio: {promedio:.2f})")
    else:
        print("  No hay alumnos en riesgo.")

    print("=========================================")


def mostrar_menu():
    print("\n1. Agregar alumno")
    print("2. Mostrar ranking")
    print("3. Salir")


def main():
    calificaciones = {}

    while True:
        mostrar_menu()
        opcion = input("Elegí una opcion: ")

        if opcion == "1":
            agregar_alumno(calificaciones)
        elif opcion == "2":
            mostrar_ranking(calificaciones)
        elif opcion == "3":
            break
        else:
            print("Opcion invalida. Probá nuevamente.")


if __name__ == "__main__":
    main()
