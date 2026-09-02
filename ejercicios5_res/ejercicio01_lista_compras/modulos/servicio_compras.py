"""Lógica de la lista de compras, separada de la interfaz gráfica.

Acá vive todo lo que es "pensar": agregar, marcar, eliminar y armar el
resumen. La ventana de Dear PyGui solo se encarga de llamar a estas
funciones y mostrar los resultados en pantalla.
"""

# Estado que comparten todos los callbacks de la ventana.
pendientes = []      # ítems que todavía hay que comprar (lista)
comprados = set()    # ítems ya comprados (conjunto, sin duplicados)


def formatear_item(item):
    """Limpia espacios extra y capitaliza cada palabra del ítem."""
    return " ".join(item.strip().split()).title()


def agregar_item(item):
    """Agrega un ítem a la lista pendiente. Evita duplicados.

    Devuelve una tupla (ok, mensaje) para que la interfaz decida qué
    mostrar y si tiene sentido limpiar el campo de texto.
    """
    item = formatear_item(item)

    if not item:
        return False, "Escribí un ítem antes de presionar el botón."

    if item in pendientes:
        return False, f"'{item}' ya está en la lista de compras."

    pendientes.append(item)
    return True, f"'{item}' fue agregado correctamente."


def marcar_comprado(item):
    """Mueve un ítem de pendientes al conjunto de comprados."""
    item = formatear_item(item)

    if item not in pendientes:
        return False, f"No se encontró '{item}' en la lista pendiente."

    pendientes.remove(item)
    comprados.add(item)
    return True, f"'{item}' fue marcado como comprado."


def eliminar_item(item):
    """Elimina un ítem pendiente de la lista."""
    item = formatear_item(item)

    if item in pendientes:
        pendientes.remove(item)
        return True, f"'{item}' fue eliminado de la lista."

    return False, f"No se puede eliminar '{item}' porque no está en la lista."


def resumen():
    """Arma el resumen formateado, listo para mostrarse en la GUI."""
    texto = "========== LISTA DE COMPRAS ==========\n"
    texto += f"Pendientes ({len(pendientes)}):\n"
    for item in pendientes:
        texto += f"  - {item}\n"

    texto += f"\nYa comprados ({len(comprados)}):\n"
    for item in sorted(comprados):
        texto += f"  - {item}\n"

    texto += "======================================"
    return texto