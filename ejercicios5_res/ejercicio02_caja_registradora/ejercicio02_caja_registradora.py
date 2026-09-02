"""Ejercicio 2 - Simulador de caja registradora con ticket.

Migración del TP 10 (caja registradora) a Dear PyGui.
La lógica vive en `modulos/servicio_caja.py`; esta ventana carga los
productos y muestra el ticket formateado en un área de texto.
"""

from dearpygui import dearpygui as dpg

from modulos.servicio_caja import (
    agregar_item,
    generar_ticket,
    items_texto,
    nueva_compra,
)


def refrescar_productos():
    """Redibuja el panel con los productos cargados hasta ahora."""
    dpg.delete_item("panel_productos", children_only=True)
    dpg.add_text(items_texto(), parent="panel_productos", wrap=360)


def al_agregar():
    """Toma los tres campos y agrega el producto a la compra."""
    ok, mensaje = agregar_item(
        dpg.get_value("input_nombre"),
        dpg.get_value("input_categoria"),
        dpg.get_value("input_precio"),
    )
    dpg.set_value("txt_estado", mensaje)

    if ok:
        dpg.set_value("input_nombre", "")
        dpg.set_value("input_categoria", "")
        dpg.set_value("input_precio", "")
    refrescar_productos()


def al_generar_ticket():
    """Muestra el ticket formateado en el área de texto."""
    dpg.set_value("txt_ticket", generar_ticket())


def al_nueva_compra():
    """Limpia todo y habilita el registro de un nuevo ticket."""
    nueva_compra()
    dpg.set_value("txt_estado", "Compra reiniciada.")
    dpg.set_value("txt_ticket", "")
    dpg.set_value("input_nombre", "")
    dpg.set_value("input_categoria", "")
    dpg.set_value("input_precio", "")
    refrescar_productos()


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
    dpg.add_text(items_texto(), wrap=360, parent="panel_productos")

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
