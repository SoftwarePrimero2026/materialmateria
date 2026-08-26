"""Ejercicio 2 - Inventario de tienda con persistencia.

La ventana inicial ya está armada. Tu tarea:
  1. Creá el módulo `modulos/servicio_inventario.py` con la lógica
     (carga del archivo, alta, venta, reposición, total, guardado) y las
     funciones del enunciado.
  2. Completá los callbacks para conectar los botones con el módulo.
"""

from dearpygui import dearpygui as dpg

# TODO: importar las funciones de la lógica
# from modulos.servicio_inventario import (
#     cargar_inventario, agregar_producto, vender, reponer,
#     listado_productos, total_inventario, guardar_inventario,
# )


def refrescar_panel():
    """Redibuja el panel con el listado de productos y el total."""
    # TODO: borrar los hijos del panel_productos y dibujar listado_productos()
    pass


def al_agregar():
    """Toma los tres campos y agrega el producto al inventario."""
    # TODO: leer input_producto / input_cantidad / input_precio -> agregar_producto()
    pass


def al_vender():
    # TODO: leer input_producto / input_cantidad -> vender()
    pass


def al_reponer():
    # TODO: leer input_producto / input_cantidad -> reponer()
    pass


def al_guardar():
    # TODO: llamar a guardar_inventario() y avisar el resultado en txt_estado
    pass


def main():
    dpg.create_context()

    dpg.create_viewport(title="Dear PyGui - Inventario", width=460, height=620)

    dpg.add_window(
        tag="ventana_principal",
        label="Inventario de tienda",
        width=440,
        height=580,
    )

    dpg.add_text("Producto, cantidad y precio:", parent="ventana_principal")
    dpg.add_input_text(tag="input_producto", label="Producto", width=300, parent="ventana_principal")
    dpg.add_input_text(tag="input_cantidad", label="Cantidad", width=300, parent="ventana_principal")
    dpg.add_input_text(tag="input_precio", label="Precio unitario ($)", width=300, parent="ventana_principal")

    dpg.add_button(label="Agregar producto", callback=al_agregar, parent="ventana_principal")
    dpg.add_button(label="Vender", callback=al_vender, parent="ventana_principal")
    dpg.add_button(label="Reponer", callback=al_reponer, parent="ventana_principal")
    dpg.add_button(label="Guardar", callback=al_guardar, parent="ventana_principal")

    dpg.add_spacer(height=6, parent="ventana_principal")
    dpg.add_text("", tag="txt_estado", wrap=400, parent="ventana_principal")

    dpg.add_separator(parent="ventana_principal")
    dpg.add_text("Listado de productos:", parent="ventana_principal")
    dpg.add_child_window(
        tag="panel_productos",
        parent="ventana_principal",
        width=405,
        height=180,
        border=True,
    )
    dpg.add_text("Acá aparecen los productos con su stock...", wrap=370, parent="panel_productos")

    dpg.setup_dearpygui()
    dpg.set_primary_window("ventana_principal", True)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()