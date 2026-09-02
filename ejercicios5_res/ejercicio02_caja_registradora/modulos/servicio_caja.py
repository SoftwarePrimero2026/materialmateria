"""Lógica del simulador de caja registradora, separada de la interfaz.

Replica el TP 10 pero pensada para que la ventana de Dear PyGui haga
todo el trabajo de entrada de datos y la salida sea un texto con el
ticket formateado.
"""

DESCUENTOS = {
    "lácteos": 0.10,
    "limpieza": 0.05,
    "panadería": 0.08,
    "verdulería": 0.12,
    "almacén": 0.04,
}

items = []  # lista de tuplas (nombre, categoria, precio)


def agregar_item(nombre, categoria, precio_texto):
    """Valida los tres datos y agrega el producto a la lista.

    Devuelve (ok, mensaje). El precio llega como texto porque viene de
    un campo de la GUI, así que hay que castearlo con defensa.
    """
    nombre = " ".join(nombre.strip().split()).title()
    categoria = categoria.strip().lower()

    try:
        precio = float(precio_texto.strip().replace(",", "."))
    except ValueError:
        return False, "El precio debe ser un número (ej: 350.50)."

    if not nombre:
        return False, "Escribí el nombre del producto."
    if not categoria:
        return False, "Escribí la categoría del producto."
    if precio <= 0:
        return False, "El precio debe ser mayor a cero."

    items.append((nombre, categoria, precio))
    return True, f"'{nombre}' cargado correctamente."


def calcular_subtotal():
    """Suma los precios de todos los ítems cargados."""
    return sum(precio for _, _, precio in items)


def calcular_descuentos():
    """Devuelve {categoria: monto_descuento} con los descuentos aplicados."""
    aplicados = {}

    for _, categoria, precio in items:
        if categoria in DESCUENTOS:
            monto = precio * DESCUENTOS[categoria]
            aplicados[categoria] = aplicados.get(categoria, 0.0) + monto

    return aplicados


def categorias_unicas():
    """Devuelve un conjunto con las categorías presentes en la compra."""
    return {categoria for _, categoria, _ in items}


def items_texto():
    """Lista los productos cargados, para el panel de la ventana."""
    if not items:
        return "Todavía no cargaste ningún producto."

    return "Productos cargados:\n" + "\n".join(
        f"  - {nombre:<16} ({categoria:<10}) $ {precio:>8.2f}"
        for nombre, categoria, precio in items
    )


def generar_ticket():
    """Arma el ticket completo con bordes, descuentos y total."""
    if not items:
        return "Cargá al menos un producto antes de generar el ticket."

    subtotal = calcular_subtotal()
    descuentos_aplicados = calcular_descuentos()
    total_descuentos = sum(descuentos_aplicados.values())
    total = subtotal - total_descuentos

    def linea(izq, der):
        """Une etiqueta y valor dentro del ancho fijo del ticket."""
        return f"║ {izq:<22}{der:>14} ║"

    texto = "╔" + "═" * 38 + "╗\n"
    texto += f"║{'TICKET DE COMPRA':^38}║\n"
    texto += "╠" + "═" * 38 + "╣\n"

    for nombre, categoria, precio in items:
        contenido = f"{nombre:<13} ({categoria:<10}) $ {precio:>7.2f}"
        texto += f"║ {contenido[:36]:<36} ║\n"

    texto += "╠" + "═" * 38 + "╣\n"
    texto += linea("Subtotal:", f"$ {subtotal:,.2f}") + "\n"

    for categoria, monto in descuentos_aplicados.items():
        porcentaje = int(DESCUENTOS[categoria] * 100)
        linea_dcto = f"Dto. {categoria} ({porcentaje}%):"
        texto += linea(linea_dcto, f"-${monto:,.2f}") + "\n"

    texto += "╠" + "═" * 38 + "╣\n"
    texto += linea("TOTAL:", f"$ {total:,.2f}") + "\n"
    texto += linea("Categorías compradas:", str(len(categorias_unicas()))) + "\n"
    texto += "╚" + "═" * 38 + "╝"

    return texto


def nueva_compra():
    """Vacía la lista de ítems para empezar un ticket nuevo."""
    items.clear()