"""Ejercicio 5 - Control de gastos con presupuesto y alertas.

Migración del Ejercicio 4 de `ejercicios4/` a Dear PyGui.
Incluye un combo para elegir la categoría, registro de gastos y un
resumen que se actualiza solo, avisando cuando se pasa el presupuesto.
"""

from dearpygui import dearpygui as dpg

from modulos.servicio_gastos import (
    PRESUPUESTOS,
    agregar_gasto,
    resumen_general,
)


def refrescar_resumen():
    """Redibuja el panel con el resumen general actualizado."""
    dpg.delete_item("panel_resumen", children_only=True)
    dpg.add_text(resumen_general(), parent="panel_resumen", wrap=430)


def al_registrar():
    """Toma los campos del formulario y registra el gasto."""
    ok, mensaje = agregar_gasto(
        dpg.get_value("combo_categoria"),
        dpg.get_value("input_monto"),
        dpg.get_value("input_descripcion"),
    )
    dpg.set_value("txt_estado", mensaje)

    if ok:
        dpg.set_value("input_monto", "")
        dpg.set_value("input_descripcion", "")
        refrescar_resumen()


def main():
    dpg.create_context()

    dpg.create_viewport(title="Dear PyGui - Control de gastos", width=520, height=560)

    dpg.add_window(
        tag="ventana_principal",
        label="Control de gastos",
        width=500,
        height=520,
    )

    dpg.add_text("Registrar gasto:", parent="ventana_principal")
    dpg.add_combo(
        tag="combo_categoria",
        items=list(PRESUPUESTOS),
        label="Categoría",
        default_value="comida",
        width=260,
        parent="ventana_principal",
    )
    dpg.add_input_text(tag="input_monto", label="Monto ($)", width=260, parent="ventana_principal")
    dpg.add_input_text(tag="input_descripcion", label="Descripción breve", width=260, parent="ventana_principal")
    dpg.add_button(label="Registrar gasto", callback=al_registrar, parent="ventana_principal")

    dpg.add_spacer(height=6, parent="ventana_principal")
    dpg.add_text("", tag="txt_estado", wrap=460, parent="ventana_principal")

    dpg.add_separator(parent="ventana_principal")
    dpg.add_text("Resumen:", parent="ventana_principal")
    dpg.add_child_window(
        tag="panel_resumen",
        parent="ventana_principal",
        width=470,
        height=250,
        border=True,
    )
    dpg.add_text(resumen_general(), wrap=430, parent="panel_resumen")

    dpg.setup_dearpygui()
    dpg.set_primary_window("ventana_principal", True)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
