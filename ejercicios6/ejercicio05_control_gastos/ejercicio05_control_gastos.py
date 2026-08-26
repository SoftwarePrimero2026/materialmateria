"""Ejercicio 5 - Control de gastos con historial guardado.

La ventana inicial ya está armada. Tu tarea:
  1. Creá el módulo `modulos/servicio_gastos.py` con la lógica
     (presupuestos, carga del archivo, validación, excesos, resumen,
     guardado) y las funciones del enunciado.
  2. Completá los callbacks para conectar el formulario con el módulo.
"""

from dearpygui import dearpygui as dpg

# TODO: importar las funciones y los presupuestos de la lógica
# from modulos.servicio_gastos import (
#     PRESUPUESTOS, cargar_gastos, agregar_gasto, resumen_general,
#     guardar_gastos,
# )


def refrescar_resumen():
    """Redibuja el panel con el resumen general actualizado."""
    # TODO: borrar hijos del panel_resumen y dibujar resumen_general()
    pass


def al_registrar():
    """Toma los campos del formulario y registra el gasto."""
    # TODO: leer combo_categoria / input_monto / input_descripcion -> agregar_gasto()
    pass


def al_guardar():
    # TODO: llamar a guardar_gastos() y avisar el resultado en txt_estado
    pass


def main():
    dpg.create_context()

    dpg.create_viewport(title="Dear PyGui - Control de gastos", width=520, height=580)

    dpg.add_window(
        tag="ventana_principal",
        label="Control de gastos",
        width=500,
        height=540,
    )

    dpg.add_text("Registrar gasto:", parent="ventana_principal")
    dpg.add_combo(
        tag="combo_categoria",
        items=["comida", "transporte", "ocio"],
        label="Categoría",
        default_value="comida",
        width=260,
        parent="ventana_principal",
    )
    dpg.add_input_text(tag="input_monto", label="Monto ($)", width=260, parent="ventana_principal")
    dpg.add_input_text(tag="input_descripcion", label="Descripción breve", width=260, parent="ventana_principal")
    dpg.add_button(label="Registrar gasto", callback=al_registrar, parent="ventana_principal")
    dpg.add_button(label="Guardar", callback=al_guardar, parent="ventana_principal")

    dpg.add_spacer(height=6, parent="ventana_principal")
    dpg.add_text("", tag="txt_estado", wrap=460, parent="ventana_principal")

    dpg.add_separator(parent="ventana_principal")
    dpg.add_text("Resumen:", parent="ventana_principal")
    dpg.add_child_window(
        tag="panel_resumen",
        parent="ventana_principal",
        width=470,
        height=280,
        border=True,
    )
    dpg.add_text("Acá va a aparecer el resumen del mes...", wrap=430, parent="panel_resumen")

    dpg.setup_dearpygui()
    dpg.set_primary_window("ventana_principal", True)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()