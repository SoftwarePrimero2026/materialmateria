# =============================================================================
# TP 10 — Simulador de caja registradora
# =============================================================================
#
# ENUNCIADO:
#   El usuario carga ítems de compra ingresando nombre, categoría y precio.
#   El programa aplica descuentos por categoría, calcula el total y emite
#   un ticket formateado.
#
# ESTRUCTURAS A UTILIZAR:
#   - Lista       : para almacenar los ítems de la compra como tuplas.
#   - Tuplas      : cada ítem es (nombre, categoría, precio).
#   - Diccionario : tabla de descuentos por categoría.
#   - Conjunto    : para registrar las categorías únicas presentes.
#   - Funciones   : una por cada parte del procesamiento.
#
# ENTRADA DE DATOS (input):
#   - El usuario ingresa nombre, categoría y precio de cada ítem.
#   - El proceso se repite hasta que el usuario indique que terminó.
#
# SALIDA (print formateado):
#   - Ticket con bordes usando caracteres Unicode (╔ ║ ╚ ═ ╠ ╣).
#
# EJEMPLO DE SALIDA ESPERADA:
#   ╔══════════════════════════════════════╗
#   ║         TICKET DE COMPRA            ║
#   ╠══════════════════════════════════════╣
#   ║  Leche 1L       (lácteos)   $ 350   ║
#   ║  Yogur x4       (lácteos)   $ 620   ║
#   ║  Lavandina      (limpieza)  $ 480   ║
#   ╠══════════════════════════════════════╣
#   ║  Subtotal:             $ 1450.00    ║
#   ║  Dto. lácteos (10%):  -$   97.00   ║
#   ║  Dto. limpieza (5%):  -$   24.00   ║
#   ╠══════════════════════════════════════╣
#   ║  TOTAL:                $ 1329.00   ║
#   ║  Categorías compradas: 2            ║
#   ╚══════════════════════════════════════╝
#
# INDICACIONES:
#   1. Definir en el código el diccionario de descuentos:
#        descuentos = {"lácteos": 0.10, "limpieza": 0.05, "panadería": 0.08, ...}
#   2. Implementar las funciones:
#        - cargar_items()                        → retorna lista de tuplas
#        - calcular_subtotal(items)              → retorna float
#        - calcular_descuentos(items, descuentos)→ retorna dict {categoria: monto}
#        - categorias_unicas(items)              → retorna un conjunto
#        - imprimir_ticket(items, descuentos_aplicados)
#   3. Si la categoría ingresada no está en el diccionario de descuentos,
#      no se aplica descuento pero el ítem se incluye igualmente.
#   4. El ticket debe estar centrado dentro de los bordes.
#
# =============================================================================

# Escribí tu código a partir de aquí:

DESCUENTOS = {
    "lácteos": 0.10,
    "limpieza": 0.05,
    "panadería": 0.08,
    "verdulería": 0.12,
    "almacén": 0.04,
}


def cargar_items():
    """Carga items hasta que el usuario indique que termino."""
    items = []

    while True:
        nombre = input("Producto: ").strip()
        categoria = input("Categoría: ").strip().lower()
        precio = float(input("Precio: $ "))

        items.append((nombre, categoria, precio))

        continuar = input("Querés cargar otro item? (s/n): ").lower()
        if continuar != "s":
            break

    return items


def calcular_subtotal(items):
    """Suma los precios de todos los items."""
    total = 0
    for nombre, categoria, precio in items:
        total += precio
    return total


def calcular_descuentos(items, descuentos):
    """Calcula el descuento total por cada categoria."""
    aplicados = {}

    for nombre, categoria, precio in items:
        if categoria in descuentos:
            monto = precio * descuentos[categoria]
            if categoria in aplicados:
                aplicados[categoria] += monto
            else:
                aplicados[categoria] = monto

    return aplicados


def categorias_unicas(items):
    """Devuelve las categorias sin repetidos."""
    categorias = set()
    for nombre, categoria, precio in items:
        categorias.add(categoria)
    return categorias


def linea_ticket(texto):
    """Centra una linea dentro del ancho del ticket."""
    print(f"║{texto:^38}║")


def imprimir_ticket(items, descuentos_aplicados):
    """Imprime el ticket con subtotal, descuentos y total."""
    subtotal = calcular_subtotal(items)
    total_descuentos = sum(descuentos_aplicados.values())
    total = subtotal - total_descuentos

    print("╔" + "═" * 38 + "╗")
    linea_ticket("TICKET DE COMPRA")
    print("╠" + "═" * 38 + "╣")

    for nombre, categoria, precio in items:
        texto = f"{nombre:<14} ({categoria:<10}) $ {precio:>7.2f}"
        print(f"║ {texto[:36]:<36} ║")

    print("╠" + "═" * 38 + "╣")
    print(f"║ {'Subtotal:':<22}$ {subtotal:>10.2f} ║")

    for categoria, monto in descuentos_aplicados.items():
        porcentaje = int(DESCUENTOS[categoria] * 100)
        texto = f"Dto. {categoria} ({porcentaje}%):"
        print(f"║ {texto:<22}-$ {monto:>9.2f} ║")

    print("╠" + "═" * 38 + "╣")
    print(f"║ {'TOTAL:':<22}$ {total:>10.2f} ║")
    print(f"║ {'Categorías compradas:':<22}{len(categorias_unicas(items)):>12} ║")
    print("╚" + "═" * 38 + "╝")


def main():
    items = cargar_items()
    descuentos_aplicados = calcular_descuentos(items, DESCUENTOS)
    imprimir_ticket(items, descuentos_aplicados)


if __name__ == "__main__":
    main()
