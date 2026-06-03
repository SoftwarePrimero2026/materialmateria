# =============================================================================
# TP 4 — Registro de temperaturas semanales
# =============================================================================
#
# ENUNCIADO:
#   El usuario ingresa las temperaturas máxima y mínima de cada día de la
#   semana. El programa almacena los datos y calcula estadísticas.
#
# ESTRUCTURAS A UTILIZAR:
#   - Lista  : para almacenar las tuplas de cada día.
#   - Tuplas : cada elemento de la lista es (día, temp_max, temp_min).
#   - Funciones : una por cada cálculo estadístico.
#
# ENTRADA DE DATOS (input):
#   - Para cada uno de los 7 días, el usuario ingresa temp_max y temp_min.
#   - El usuario también ingresa el umbral de amplitud térmica a consultar.
#
# SALIDA (print formateado):
#   - Tabla semanal con columnas alineadas.
#   - Resumen de promedios, día más caluroso, más frío y días con alta amplitud.
#
# EJEMPLO DE SALIDA ESPERADA:
#   ======= RESUMEN SEMANAL DE TEMPERATURAS =======
#   Día           Máx     Mín     Amplitud
#   -----------------------------------------------
#   Lunes         28°C    15°C    13°C
#   Martes        31°C    18°C    13°C
#   Miércoles     25°C    12°C    13°C  ← mayor amplitud
#   ...
#   Promedios:  Máx 27.4°C  |  Mín 14.8°C
#   Día más caluroso:  Martes (31°C)
#   Día más frío:      Miércoles (12°C)
#   Días con amplitud > 12°C: Lunes, Martes, Miércoles
#   ===============================================
#
# INDICACIONES:
#   1. Definir la lista de días de la semana en el código.
#   2. Implementar las funciones:
#        - cargar_temperaturas()           → retorna lista de tuplas
#        - promedio_maximas(registros)     → retorna float
#        - promedio_minimas(registros)     → retorna float
#        - dia_mas_caluroso(registros)     → retorna tupla del día más caluroso
#        - dia_mas_frio(registros)         → retorna tupla del día más frío
#        - dias_alta_amplitud(registros, umbral) → retorna lista de días
#        - mostrar_tabla(registros)        → imprime la tabla formateada
#   3. Validar que temp_max >= temp_min al cargar datos.
#   4. Marcar con "← mayor amplitud" la fila correspondiente en la tabla.
#
# =============================================================================

# Escribí tu código a partir de aquí:

# -----------------------------------------------------------------------------
# Datos fijos del programa
# -----------------------------------------------------------------------------

# Lista con los nombres de los días de la semana.
DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

# Estados del cielo válidos que el usuario puede cargar.
# Usamos un número para que sea más fácil elegir y no tener que escribir todo.
ESTADOS_CIELO = {
    "1": "Soleado",
    "2": "Parcialmente nublado",
    "3": "Nublado",
}


# -----------------------------------------------------------------------------
# Funciones de entrada de datos
# -----------------------------------------------------------------------------

def pedir_estado_cielo(dia):
    """Pide al usuario el estado del cielo de un día y lo devuelve como texto.

    Repite la pregunta hasta que ingrese una opción válida (1, 2 o 3).
    """
    print("  Estado del cielo:")
    print("    1 - Soleado")
    print("    2 - Parcialmente nublado")
    print("    3 - Nublado")

    while True:
        opcion = input(f"  Elegí una opción (1-3) para el {dia}: ")
        if opcion in ESTADOS_CIELO:
            return ESTADOS_CIELO[opcion]
        print("  Opción inválida. Tenés que ingresar 1, 2 o 3.")


def cargar_temperaturas():
    """Pide los datos de cada día y devuelve una lista de tuplas.

    Cada tupla tiene la forma: (día, temp_max, temp_min, estado_cielo)
    """
    registros = []

    for dia in DIAS:
        print(f"\n--- {dia} ---")

        # Pedimos las temperaturas validando que max >= min.
        while True:
            temp_max = float(input(f"  Temperatura máxima de {dia}: "))
            temp_min = float(input(f"  Temperatura mínima de {dia}: "))

            if temp_max >= temp_min:
                break
            print("  Error: la máxima no puede ser menor que la mínima. Volvé a cargar.")

        # Pedimos el estado del cielo.
        estado = pedir_estado_cielo(dia)

        # Guardamos la tupla completa en la lista.
        registros.append((dia, temp_max, temp_min, estado))

    return registros


# -----------------------------------------------------------------------------
# Funciones de cálculo estadístico
# -----------------------------------------------------------------------------

def promedio_maximas(registros):
    """Devuelve el promedio de las temperaturas máximas."""
    suma = 0
    for dia, temp_max, temp_min, estado in registros:
        suma += temp_max
    return suma / len(registros)


def promedio_minimas(registros):
    """Devuelve el promedio de las temperaturas mínimas."""
    suma = 0
    for dia, temp_max, temp_min, estado in registros:
        suma += temp_min
    return suma / len(registros)


def dia_mas_caluroso(registros):
    """Devuelve la tupla del día con la temperatura máxima más alta."""
    mas_caluroso = registros[0]
    for registro in registros:
        # registro[1] es la temp_max de ese día.
        if registro[1] > mas_caluroso[1]:
            mas_caluroso = registro
    return mas_caluroso


def dia_mas_frio(registros):
    """Devuelve la tupla del día con la temperatura mínima más baja."""
    mas_frio = registros[0]
    for registro in registros:
        # registro[2] es la temp_min de ese día.
        if registro[2] < mas_frio[2]:
            mas_frio = registro
    return mas_frio


def dias_alta_amplitud(registros, umbral):
    """Devuelve una lista con los nombres de los días cuya amplitud supera el umbral."""
    dias = []
    for dia, temp_max, temp_min, estado in registros:
        amplitud = temp_max - temp_min
        if amplitud > umbral:
            dias.append(dia)
    return dias


def amplitud_maxima(registros):
    """Devuelve el valor de la mayor amplitud térmica de la semana."""
    mayor = 0
    for dia, temp_max, temp_min, estado in registros:
        amplitud = temp_max - temp_min
        if amplitud > mayor:
            mayor = amplitud
    return mayor


# -----------------------------------------------------------------------------
# Funciones de salida
# -----------------------------------------------------------------------------

def mostrar_tabla(registros):
    """Imprime la tabla semanal formateada con columnas alineadas."""
    print("\n======= RESUMEN SEMANAL DE TEMPERATURAS =======")
    print(f"{'Día':<12}{'Máx':<8}{'Mín':<8}{'Amplitud':<10}{'Cielo':<22}")
    print("-" * 60)

    mayor_amplitud = amplitud_maxima(registros)

    for dia, temp_max, temp_min, estado in registros:
        amplitud = temp_max - temp_min

        # Armamos cada columna con su formato.
        col_dia = f"{dia:<12}"
        col_max = f"{temp_max:.0f}°C".ljust(8)
        col_min = f"{temp_min:.0f}°C".ljust(8)
        col_amp = f"{amplitud:.0f}°C".ljust(10)
        col_cielo = f"{estado:<22}"

        # Marcamos la fila con la mayor amplitud.
        marca = "← mayor amplitud" if amplitud == mayor_amplitud else ""

        print(col_dia + col_max + col_min + col_amp + col_cielo + marca)

    print("-" * 60)


def mostrar_resumen(registros, umbral):
    """Imprime los promedios y los días destacados."""
    prom_max = promedio_maximas(registros)
    prom_min = promedio_minimas(registros)
    caluroso = dia_mas_caluroso(registros)
    frio = dia_mas_frio(registros)
    altos = dias_alta_amplitud(registros, umbral)

    print(f"Promedios:  Máx {prom_max:.1f}°C  |  Mín {prom_min:.1f}°C")
    print(f"Día más caluroso:  {caluroso[0]} ({caluroso[1]:.0f}°C)")
    print(f"Día más frío:      {frio[0]} ({frio[2]:.0f}°C)")

    if altos:
        print(f"Días con amplitud > {umbral:.0f}°C: {', '.join(altos)}")
    else:
        print(f"Días con amplitud > {umbral:.0f}°C: ninguno")

    print("===============================================")


# -----------------------------------------------------------------------------
# Programa principal
# -----------------------------------------------------------------------------

def main():
    print("Carga de temperaturas de la semana")
    registros = cargar_temperaturas()

    umbral = float(input("\nIngresá el umbral de amplitud térmica a consultar: "))

    mostrar_tabla(registros)
    mostrar_resumen(registros, umbral)


# Esta línea hace que main() se ejecute solo si corremos este archivo.
if __name__ == "__main__":
    main()
