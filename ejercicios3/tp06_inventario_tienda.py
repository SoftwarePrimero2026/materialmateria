# =============================================================================
# TP 6 — Inventario de una tienda
# =============================================================================
#
# ENUNCIADO:
#   Modelar el inventario de una tienda. Cada producto tiene precio y stock.
#   El programa permite registrar ventas, reponer stock y ver estadísticas.
#
# ESTRUCTURAS A UTILIZAR:
#   - Diccionario : clave = nombre del producto (str).
#   - Tupla       : valor = (precio, stock) por cada producto.
#   - Funciones   : una por cada operación.
#
# ENTRADA DE DATOS (input):
#   - Los datos iniciales se definen en el código.
#   - El usuario elige qué operación realizar a través de un menú.
#   - Para ventas y reposición, el usuario ingresa el producto y la cantidad.
#
# SALIDA (print formateado):
#   - Tabla del inventario con columnas alineadas.
#   - Indicación visual (⚠) junto a productos con bajo stock.
#   - Valor total del inventario al pie.
#
# EJEMPLO DE SALIDA ESPERADA:
#   ========== INVENTARIO DE LA TIENDA ==========
#   Producto         Precio      Stock    Valor
#   ---------------------------------------------
#   Café 500g        $ 850.00    12       $ 10200.00
#   Azúcar 1kg       $ 430.00    3   ⚠    $  1290.00
#   Yerba 500g       $ 920.00    8        $  7360.00
#   ---------------------------------------------
#   Valor total del inventario:  $ 18850.00
#
#   ⚠ Productos con bajo stock (< 5):
#     · Azúcar 1kg (3 unidades)
#   =============================================
#
# INDICACIONES:
#   1. Definir al menos 5 productos en el inventario inicial.
#   2. Implementar las funciones:
#        - registrar_venta(inventario, producto, cantidad)
#        - reponer_stock(inventario, producto, cantidad)
#        - productos_bajo_stock(inventario, umbral)  → retorna lista
#        - valor_total(inventario)                   → retorna float
#        - mostrar_inventario(inventario)             → imprime tabla
#   3. No permitir ventas si el stock es insuficiente.
#   4. Las tuplas son inmutables: al actualizar precio o stock, se debe
#      reemplazar la tupla completa en el diccionario.
#
# =============================================================================

# Escribí tu código a partir de aquí:

UMBRAL_BAJO_STOCK = 5


def registrar_venta(inventario, producto, cantidad):
    """Descuenta stock si el producto existe y alcanza la cantidad."""
    if producto not in inventario:
        print("Producto no encontrado.")
        return

    precio, stock = inventario[producto]
    if cantidad > stock:
        print("No hay stock suficiente para esa venta.")
        return

    inventario[producto] = (precio, stock - cantidad)
    print("Venta registrada correctamente.")


def reponer_stock(inventario, producto, cantidad):
    """Suma unidades al stock actual del producto."""
    if producto not in inventario:
        print("Producto no encontrado.")
        return

    precio, stock = inventario[producto]
    inventario[producto] = (precio, stock + cantidad)
    print("Stock actualizado correctamente.")


def productos_bajo_stock(inventario, umbral):
    """Devuelve productos con stock menor al umbral."""
    bajos = []
    for producto, datos in inventario.items():
        precio, stock = datos
        if stock < umbral:
            bajos.append((producto, stock))
    return bajos


def valor_total(inventario):
    """Calcula el valor total del inventario."""
    total = 0
    for precio, stock in inventario.values():
        total += precio * stock
    return total


def mostrar_inventario(inventario):
    """Muestra una tabla con precio, stock y valor por producto."""
    print("\n========== INVENTARIO DE LA TIENDA ==========")
    print(f"{'Producto':<18}{'Precio':<12}{'Stock':<9}{'Valor'}")
    print("---------------------------------------------")

    for producto, datos in sorted(inventario.items()):
        precio, stock = datos
        valor = precio * stock
        alerta = "⚠" if stock < UMBRAL_BAJO_STOCK else ""
        print(f"{producto:<18}$ {precio:<10.2f}{stock:<5} {alerta:<3}$ {valor:>9.2f}")

    print("---------------------------------------------")
    print(f"Valor total del inventario:  $ {valor_total(inventario):.2f}")

    bajos = productos_bajo_stock(inventario, UMBRAL_BAJO_STOCK)
    print(f"\n⚠ Productos con bajo stock (< {UMBRAL_BAJO_STOCK}):")
    if bajos:
        for producto, stock in bajos:
            print(f"  · {producto} ({stock} unidades)")
    else:
        print("  No hay productos con bajo stock.")
    print("=============================================")


def mostrar_menu():
    print("\n1. Registrar venta")
    print("2. Reponer stock")
    print("3. Mostrar inventario")
    print("4. Salir")


def main():
    inventario = {
        "Café 500g": (850.00, 12),
        "Azúcar 1kg": (430.00, 3),
        "Yerba 500g": (920.00, 8),
        "Galletitas": (650.00, 4),
        "Fideos": (510.00, 15),
    }

    while True:
        mostrar_menu()
        opcion = input("Elegí una opcion: ")

        if opcion == "1":
            producto = input("Producto: ").strip()
            cantidad = int(input("Cantidad vendida: "))
            registrar_venta(inventario, producto, cantidad)
        elif opcion == "2":
            producto = input("Producto: ").strip()
            cantidad = int(input("Cantidad a reponer: "))
            reponer_stock(inventario, producto, cantidad)
        elif opcion == "3":
            mostrar_inventario(inventario)
        elif opcion == "4":
            break
        else:
            print("Opcion invalida. Probá nuevamente.")


if __name__ == "__main__":
    main()
