# =====================================================================
# Ejercicio 4 — Control de gastos personales
# Solución de referencia (para corrección)
# Conceptos: archivos, diccionarios, listas de tuplas, ciclos,
#            decisiones, funciones, acumuladores, try/except.
# =====================================================================

# Presupuesto mensual asignado a cada categoría (definido en el código).
PRESUPUESTO = {
    "comida": 50000.0,
    "transporte": 20000.0,
    "ocio": 15000.0,
}

# Archivo donde se guardan/leen los gastos cargados.
ARCHIVO_GASTOS = "gastos.txt"


def leer_gastos():
    """Lee los gastos del archivo. Devuelve una lista de tuplas
    (categoria, monto, descripcion). Si no existe, lista vacía."""
    gastos = []
    try:
        with open(ARCHIVO_GASTOS, "r") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea == "":
                    continue
                categoria, monto, descripcion = linea.split(";")
                gastos.append((categoria, float(monto), descripcion))
    except FileNotFoundError:
        # Primera vez: no hay gastos cargados todavía.
        pass
    return gastos


def guardar_gastos(gastos):
    """Guarda todos los gastos en el archivo, sobrescribiendo."""
    with open(ARCHIVO_GASTOS, "w") as archivo:
        for categoria, monto, descripcion in gastos:
            archivo.write(f"{categoria};{monto};{descripcion}\n")


def total_por_categoria(gastos, categoria):
    """Suma todos los montos gastados en una categoría."""
    total = 0.0
    for cat, monto, _descripcion in gastos:
        if cat == categoria:
            total += monto
    return total


def registrar_gasto(gastos):
    """Pide los datos de un gasto, lo valida y lo agrega a la lista."""
    categoria = input("Categoría: ").strip().lower()
    # Solo se aceptan categorías que existan en el presupuesto.
    if categoria not in PRESUPUESTO:
        print(f"La categoría '{categoria}' no existe en el presupuesto.")
        return

    # Pedimos el monto validando que sea un número mayor a cero.
    while True:
        try:
            monto = float(input("Monto: $"))
            if monto <= 0:
                print("El monto debe ser mayor a cero.")
                continue
            break
        except ValueError:
            print("Error: ingrese un número válido.")

    descripcion = input("Descripción: ").strip()
    gastos.append((categoria, monto, descripcion))
    print("Gasto registrado.")

    # Alerta inmediata si con este gasto se supera el presupuesto.
    gastado = total_por_categoria(gastos, categoria)
    if gastado > PRESUPUESTO[categoria]:
        print(f"¡Atención! Te pasaste del presupuesto de {categoria}.")


def ver_por_categoria(gastos):
    """Muestra los gastos de una categoría y el saldo disponible."""
    categoria = input("Categoría a consultar: ").strip().lower()
    if categoria not in PRESUPUESTO:
        print("Esa categoría no existe.")
        return

    print(f"\n--- Gastos en {categoria} ---")
    hubo_gastos = False
    for cat, monto, descripcion in gastos:
        if cat == categoria:
            print(f"  ${monto:.2f}  -  {descripcion}")
            hubo_gastos = True
    if not hubo_gastos:
        print("  (sin gastos en esta categoría)")

    gastado = total_por_categoria(gastos, categoria)
    restante = PRESUPUESTO[categoria] - gastado
    print(f"Total gastado: ${gastado:.2f}")
    if restante >= 0:
        print(f"Disponible:    ${restante:.2f}")
    else:
        # Si el restante es negativo, es un exceso (sobregiro).
        print(f"Exceso:        ${-restante:.2f} (te pasaste del presupuesto)")


def ver_resumen(gastos):
    """Muestra el resumen general del mes."""
    if len(gastos) == 0:
        print("No hay gastos registrados.")
        return

    total_general = 0.0
    print("\n===== RESUMEN GENERAL =====")
    print("Gasto por categoría:")
    # Recorremos cada categoría del presupuesto para mostrar su total.
    categoria_mayor = ""
    monto_mayor = -1.0
    for categoria in PRESUPUESTO:
        gastado = total_por_categoria(gastos, categoria)
        total_general += gastado
        print(f"  {categoria}: ${gastado:.2f}")

        # Detectamos en qué categoría se gastó más.
        if gastado > monto_mayor:
            monto_mayor = gastado
            categoria_mayor = categoria

        # Avisamos si se superó el presupuesto.
        if gastado > PRESUPUESTO[categoria]:
            exceso = gastado - PRESUPUESTO[categoria]
            print(f"     -> superaste el presupuesto por ${exceso:.2f}")

    print(f"\nTotal gastado en el mes: ${total_general:.2f}")
    print(f"Categoría con mayor gasto: {categoria_mayor} (${monto_mayor:.2f})")


def mostrar_menu():
    print("\n===== CONTROL DE GASTOS =====")
    print("1. Registrar un gasto")
    print("2. Ver gastos por categoría")
    print("3. Ver resumen general")
    print("4. Salir")


def main():
    gastos = leer_gastos()  # cargamos lo guardado de sesiones anteriores

    while True:
        mostrar_menu()
        opcion = input("Elija una opción: ")

        if opcion == "1":
            registrar_gasto(gastos)
        elif opcion == "2":
            ver_por_categoria(gastos)
        elif opcion == "3":
            ver_resumen(gastos)
        elif opcion == "4":
            guardar_gastos(gastos)  # persistimos antes de salir
            print("Gastos guardados. ¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


main()
