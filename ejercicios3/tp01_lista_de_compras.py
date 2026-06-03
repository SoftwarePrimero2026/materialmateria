# =============================================================================
# TP 1 — Gestión de lista de compras
# =============================================================================
#
# ENUNCIADO:
#   Crear un programa que administre una lista de compras interactiva.
#   El usuario puede agregar ítems, marcarlos como comprados, eliminarlos
#   y ver un resumen final.
#
# ESTRUCTURAS A UTILIZAR:
#   - Lista        : para almacenar los ítems pendientes de comprar.
#   - Conjunto     : para almacenar los ítems ya comprados (sin duplicados).
#   - Funciones    : cada operación debe estar en su propia función.
#
# ENTRADA DE DATOS (input):
#   - El usuario ingresa por teclado el nombre de cada ítem.
#   - El usuario elige la operación a realizar a través de un menú numérico.
#
# SALIDA (print formateado):
#   - Mostrar un resumen con separadores visuales que distinga claramente
#     los ítems pendientes de los ya comprados.
#
# EJEMPLO DE SALIDA ESPERADA:
#   ========== LISTA DE COMPRAS ==========
#   Pendientes (3):
#     - Leche
#     - Pan
#     - Arroz
#
#   Ya comprados (2):
#     - Huevos
#     - Aceite
#   ======================================
#
# INDICACIONES:
#   1. Implementar las siguientes funciones:
#        - agregar_item(lista, item)         → agrega un ítem a la lista
#        - marcar_comprado(lista, comprados, item) → mueve ítem a comprados
#        - eliminar_item(lista, item)        → elimina ítem de la lista
#        - mostrar_resumen(lista, comprados) → imprime el resumen formateado
#   2. El menú debe repetirse hasta que el usuario elija "Salir".
#   3. Controlar que no se agreguen ítems duplicados a la lista.
#   4. Si el usuario intenta marcar o eliminar un ítem que no existe,
#      mostrar un mensaje de error amigable.
#
# =============================================================================

# Escribí tu código a partir de aquí:


def agregar_item(lista, item):
    """Agrega un item si todavia no esta en la lista."""
    if item in lista:
        print(f"'{item}' ya esta en la lista de compras.")
    else:
        lista.append(item)
        print(f"'{item}' fue agregado correctamente.")


def marcar_comprado(lista, comprados, item):
    """Pasa un item de pendientes al conjunto de comprados."""
    if item in lista:
        lista.remove(item)
        comprados.add(item)
        print(f"'{item}' fue marcado como comprado.")
    else:
        print(f"No se encontro '{item}' en la lista pendiente.")


def eliminar_item(lista, item):
    """Elimina un item pendiente de la lista."""
    if item in lista:
        lista.remove(item)
        print(f"'{item}' fue eliminado.")
    else:
        print(f"No se puede eliminar '{item}' porque no esta en la lista.")


def mostrar_resumen(lista, comprados):
    """Muestra pendientes y comprados con un formato claro."""
    print("\n========== LISTA DE COMPRAS ==========")
    print(f"Pendientes ({len(lista)}):")
    for item in lista:
        print(f"  - {item}")

    print(f"\nYa comprados ({len(comprados)}):")
    for item in sorted(comprados):
        print(f"  - {item}")
    print("======================================")


def mostrar_menu():
    print("\n1. Agregar item")
    print("2. Marcar como comprado")
    print("3. Eliminar item")
    print("4. Ver resumen")
    print("5. Salir")


def main():
    pendientes = []
    comprados = set()

    while True:
        mostrar_menu()
        opcion = input("Elegí una opcion: ")

        if opcion == "1":
            item = input("Item a agregar: ").strip()
            if item:
                agregar_item(pendientes, item)
        elif opcion == "2":
            item = input("Item comprado: ").strip()
            marcar_comprado(pendientes, comprados, item)
        elif opcion == "3":
            item = input("Item a eliminar: ").strip()
            eliminar_item(pendientes, item)
        elif opcion == "4":
            mostrar_resumen(pendientes, comprados)
        elif opcion == "5":
            mostrar_resumen(pendientes, comprados)
            break
        else:
            print("Opcion invalida. Probá nuevamente.")


if __name__ == "__main__":
    main()
