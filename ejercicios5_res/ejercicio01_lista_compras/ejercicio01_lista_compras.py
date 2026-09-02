"""Ejercicio 1 - Lista de compras con interfaz gráfica.

Migración del TP 1 (gestión de lista de compras) a Dear PyGui.
La lógica vive en `modulos/servicio_compras.py`; esta ventana solo
conecta los widgets con las funciones del módulo.
"""

from dearpygui import dearpygui as dpg

from modulos.servicio_compras import (
    agregar_item,
    eliminar_item,
    marcar_comprado,
    resumen,
)


def actualizar_paneles():
    """Borra el contenido del panel resumen y lo vuelve a dibujar."""
    dpg.delete_item("panel_resumen", children_only=True)
    dpg.add_text(resumen(), parent="panel_resumen", wrap=360)


def al_agregar():
    """Lee el campo de texto, agrega el ítem y refresca la pantalla."""
    ok, mensaje = agregar_item(dpg.get_value("input_item"))
    dpg.set_value("txt_estado", mensaje)

    if ok:
        dpg.set_value("input_item", "")
    actualizar_paneles()


def al_comprar():
    """Marca el ítem del campo de texto como comprado."""
    ok, mensaje = marcar_comprado(dpg.get_value("input_item"))
    dpg.set_value("txt_estado", mensaje)

    if ok:
        dpg.set_value("input_item", "")
    actualizar_paneles()


def al_eliminar():
    """Elimina el ítem del campo de texto de la lista pendiente."""
    ok, mensaje = eliminar_item(dpg.get_value("input_item"))
    dpg.set_value("txt_estado", mensaje)

    if ok:
        dpg.set_value("input_item", "")
    actualizar_paneles()


def main():
    dpg.create_context()

    dpg.create_viewport(title="Dear PyGui - Lista de compras", width=440, height=500)

    dpg.add_window(
        tag="ventana_principal",
        label="Lista de compras",
        width=420,
        height=460,
    )

    dpg.add_text("Escribí un ítem y elegí una acción:", parent="ventana_principal")
    dpg.add_input_text(
        tag="input_item",
        label="Ítem",
        width=320,
        callback=al_agregar,
        on_enter=True,
        parent="ventana_principal",
    )
    dpg.add_button(label="Agregar ítem", callback=al_agregar, parent="ventana_principal")
    dpg.add_button(label="Marcar como comprado", callback=al_comprar, parent="ventana_principal")
    dpg.add_button(label="Eliminar ítem", callback=al_eliminar, parent="ventana_principal")

    dpg.add_spacer(height=6, parent="ventana_principal")
    dpg.add_text("", tag="txt_estado", wrap=390, parent="ventana_principal")

    dpg.add_separator(parent="ventana_principal")
    dpg.add_text("Resumen:", parent="ventana_principal")
    dpg.add_child_window(
        tag="panel_resumen",
        parent="ventana_principal",
        width=390,
        height=200,
        border=True,
    )
    dpg.add_text(resumen(), wrap=360, parent="panel_resumen")

    dpg.setup_dearpygui()
    dpg.set_primary_window("ventana_principal", True)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
