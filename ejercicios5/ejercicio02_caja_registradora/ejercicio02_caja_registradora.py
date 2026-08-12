"""Ejercicio 2 - Simulador de caja registradora con ticket.

La ventana inicial ya está armada. Tu tarea:
  1. Creá el módulo `modulos/servicio_caja.py` con la lógica
     (descuentos, subtotal, ticket) y las funciones del enunciado.
  2. Completá los callbacks para conectar los botones con el módulo.
"""

from dearpygui import dearpygui as dpg

# TODO: importar las funciones de la lógica
# from modulos.servicio_caja import (
#     agregar_item, items_texto, generar_ticket, nueva_compra,
# )


def refrescar_productos():
    """Redibuja el panel con los productos cargados hasta ahora."""
    # TODO: borrar los hijos del panel_productos y dibujar items_texto()
    pass


def al_agregar():
    """Toma los tres campos y agrega el producto a la compra."""
    # TODO: leer input_nombre / input_categoria / input_precio y llamar a agregar_item()
    pass


def al_generar_ticket():
    # TODO: mostrar generar_ticket() en el área txt_ticket
    pass


def al_nueva_compra():
    # TODO: limpiar compra, campos y áreas
    pass


def main():
    dpg.create_context()

    dpg.create_viewport(title="Dear PyGui - Caja registradora", width=450, height=600)

    dpg.add_window(
        tag="ventana_principal",
        label="Caja registradora",
        width=430,
        height=560,
    )

    dpg.add_text("Cargá un producto:", parent="ventana_principal")
    dpg.add_input_text(tag="input_nombre", label="Producto", width=300, parent="ventana_principal")
    dpg.add_input_text(tag="input_categoria", label="Categoría", width=300, parent="ventana_principal")
    dpg.add_input_text(tag="input_precio", label="Precio", width=300, parent="ventana_principal")

    dpg.add_button(label="Agregar producto", callback=al_agregar, parent="ventana_principal")
    dpg.add_button(label="Generar ticket", callback=al_generar_ticket, parent="ventana_principal")
    dpg.add_button(label="Nueva compra", callback=al_nueva_compra, parent="ventana_principal")

    dpg.add_spacer(height=6, parent="ventana_principal")
    dpg.add_text("", tag="txt_estado", wrap=400, parent="ventana_principal")

    dpg.add_separator(parent="ventana_principal")
    dpg.add_text("Productos cargados:", parent="ventana_principal")
    dpg.add_child_window(
        tag="panel_productos",
        parent="ventana_principal",
        width=395,
        height=90,
        border=True,
    )
    dpg.add_text("Acá aparecen los productos que vas cargando...", wrap=360, parent="panel_productos")

    dpg.add_text("Ticket:", parent="ventana_principal")
    dpg.add_input_text(
        tag="txt_ticket",
        multiline=True,
        readonly=True,
        width=395,
        height=180,
        default_value="",
        parent="ventana_principal",
    )

    dpg.setup_dearpygui()
    dpg.set_primary_window("ventana_principal", True)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
