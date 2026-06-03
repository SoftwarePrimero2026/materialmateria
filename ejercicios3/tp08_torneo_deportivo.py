# =============================================================================
# TP 8 — Torneo deportivo
# =============================================================================
#
# ENUNCIADO:
#   El usuario carga los resultados de los partidos de un torneo de fútbol.
#   El programa construye y muestra la tabla de posiciones completa.
#
# ESTRUCTURAS A UTILIZAR:
#   - Lista       : para almacenar los resultados (una tupla por partido).
#   - Tuplas      : cada partido es (equipo_local, equipo_visitante, goles_l, goles_v).
#   - Diccionario : para acumular estadísticas por equipo.
#   - Funciones   : una por cada parte del procesamiento.
#
# ENTRADA DE DATOS (input):
#   - El usuario ingresa los datos de cada partido.
#   - El sistema pregunta si desea cargar otro partido hasta que el usuario indique fin.
#
# SALIDA (print formateado):
#   - Tabla de posiciones ordenada por puntos (y diferencia de goles como desempate).
#
# EJEMPLO DE SALIDA ESPERADA:
#   ============= TABLA DE POSICIONES =============
#   Pos  Equipo         PJ  G  E  P  GF  GC  Dif  Pts
#   ---------------------------------------------------
#    1   River Plate     3  2  1  0   7   3   +4    7
#    2   Boca Juniors    3  2  0  1   5   4   +1    6
#    3   Racing Club     3  0  1  2   3   6   -3    1
#   ===============================================
#
# INDICACIONES:
#   1. Implementar las funciones:
#        - cargar_partidos()                      → retorna lista de tuplas
#        - procesar_resultados(partidos)          → retorna diccionario de equipos
#        - ordenar_tabla(estadisticas)            → retorna lista ordenada
#        - mostrar_tabla(tabla_ordenada)          → imprime tabla formateada
#   2. Cada equipo en el diccionario tiene las claves:
#        "pj", "g", "e", "p", "gf", "gc", "pts"
#   3. Criterio de ordenamiento: primero por pts (desc), luego por (gf-gc) (desc).
#   4. Prefijo "+" para diferencia positiva, "-" para negativa.
#   5. Si un equipo aparece solo como visitante en todos sus partidos,
#      igual debe estar registrado en la tabla.
#
# =============================================================================

# Escribí tu código a partir de aquí:


def cargar_partidos():
    """Carga partidos hasta que el usuario decida terminar."""
    partidos = []

    while True:
        local = input("Equipo local: ").strip()
        visitante = input("Equipo visitante: ").strip()
        goles_local = int(input("Goles del local: "))
        goles_visitante = int(input("Goles del visitante: "))

        partidos.append((local, visitante, goles_local, goles_visitante))

        continuar = input("Querés cargar otro partido? (s/n): ").lower()
        if continuar != "s":
            break

    return partidos


def crear_estadisticas():
    """Devuelve el diccionario base para un equipo."""
    return {"pj": 0, "g": 0, "e": 0, "p": 0, "gf": 0, "gc": 0, "pts": 0}


def asegurar_equipo(estadisticas, equipo):
    """Agrega el equipo si todavia no existe."""
    if equipo not in estadisticas:
        estadisticas[equipo] = crear_estadisticas()


def procesar_resultados(partidos):
    """Convierte la lista de partidos en estadisticas por equipo."""
    estadisticas = {}

    for local, visitante, goles_l, goles_v in partidos:
        asegurar_equipo(estadisticas, local)
        asegurar_equipo(estadisticas, visitante)

        estadisticas[local]["pj"] += 1
        estadisticas[visitante]["pj"] += 1
        estadisticas[local]["gf"] += goles_l
        estadisticas[local]["gc"] += goles_v
        estadisticas[visitante]["gf"] += goles_v
        estadisticas[visitante]["gc"] += goles_l

        if goles_l > goles_v:
            estadisticas[local]["g"] += 1
            estadisticas[visitante]["p"] += 1
            estadisticas[local]["pts"] += 3
        elif goles_l < goles_v:
            estadisticas[visitante]["g"] += 1
            estadisticas[local]["p"] += 1
            estadisticas[visitante]["pts"] += 3
        else:
            estadisticas[local]["e"] += 1
            estadisticas[visitante]["e"] += 1
            estadisticas[local]["pts"] += 1
            estadisticas[visitante]["pts"] += 1

    return estadisticas


def ordenar_tabla(estadisticas):
    """Ordena por puntos y luego por diferencia de goles."""
    tabla = list(estadisticas.items())
    tabla.sort(key=lambda dato: (dato[1]["pts"], dato[1]["gf"] - dato[1]["gc"]), reverse=True)
    return tabla


def mostrar_tabla(tabla_ordenada):
    """Imprime la tabla de posiciones."""
    if not tabla_ordenada:
        print("No hay partidos cargados.")
        return

    print("\n============= TABLA DE POSICIONES =============")
    print(f"{'Pos':<5}{'Equipo':<16}{'PJ':<4}{'G':<3}{'E':<3}{'P':<3}{'GF':<4}{'GC':<4}{'Dif':<6}{'Pts'}")
    print("---------------------------------------------------")

    for posicion, dato in enumerate(tabla_ordenada, start=1):
        equipo, estadistica = dato
        diferencia = estadistica["gf"] - estadistica["gc"]
        diferencia_texto = f"{diferencia:+d}"
        print(
            f"{posicion:<5}{equipo:<16}{estadistica['pj']:<4}{estadistica['g']:<3}"
            f"{estadistica['e']:<3}{estadistica['p']:<3}{estadistica['gf']:<4}"
            f"{estadistica['gc']:<4}{diferencia_texto:<6}{estadistica['pts']}"
        )

    print("===============================================")


def main():
    partidos = cargar_partidos()
    estadisticas = procesar_resultados(partidos)
    tabla = ordenar_tabla(estadisticas)
    mostrar_tabla(tabla)


if __name__ == "__main__":
    main()
