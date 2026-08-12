"""Ejercicio 1 - Lista de compras con interfaz gráfica.

La ventana inicial ya está armada. Tu tarea:
  1. Creá el módulo `modulos/servicio_compras.py` con la lógica
     (lista pendiente + conjunto de comprados) y las funciones del enunciado.
  2. Completá los callbacks para conectar los botones con el módulo.
"""

from dearpygui import dearpygui as dpg

# TODO: importar las funciones de la lógica
# from modulos.servicio_compras import agregar_item, marcar_comprado, eliminar_item, resumen


def actualizar_paneles():
    """Refresca el panel con el resumen de la lista completa."""
    # TODO: borrar los hijos del panel_resumen y volver a dibujar el resumen
    pass


def al_agregar():
    """Lee el campo, agrega el ítem y refresca la pantalla."""
    # TODO: dpg.get_value("input_item") -> agregar_item -> dpg.set_value("txt_estado", mensaje)
    pass


def al_comprar():
    # TODO: marcar el ítem del campo como comprado y refrescar
    pass


def al_eliminar():
    # TODO: eliminar el ítem del campo y refrescar
    pass


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
    dpg.add_input_text(tag="input_item", label="Ítem", width=320, parent="ventana_principal")

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
    dpg.add_text("Acá va a aparecer el resumen de tu lista...", wrap=360, parent="panel_resumen")

    dpg.setup_dearpygui()
    dpg.set_primary_window("ventana_principal", True)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
