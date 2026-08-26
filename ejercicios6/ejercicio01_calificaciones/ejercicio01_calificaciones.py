"""Ejercicio 1 - Planilla de calificaciones que se guarda.

La ventana inicial ya está armada. Tu tarea:
  1. Creá el módulo `modulos/servicio_notas.py` con la lógica
     (carga del archivo, alta de notas, resumen, guardado) y las funciones
     del enunciado.
  2. Completá los callbacks para conectar los botones con el módulo.
"""

from dearpygui import dearpygui as dpg

# TODO: importar las funciones de la lógica
# from modulos.servicio_notas import (
#     cargar_notas, agregar_nota, resumen, guardar_notas,
# )


def refrescar_panel():
    """Redibuja el panel con la lista de alumnos y notas cargadas."""
    # TODO: borrar los hijos del panel_notas y dibujar la lista actual
    pass


def al_agregar():
    """Toma los dos campos y agrega la nota del alumno."""
    # TODO: leer input_alumno / input_nota -> agregar_nota() -> refrescar_panel()
    pass


def al_ver_resumen():
    # TODO: mostrar resumen() en el área txt_resumen
    pass


def al_guardar():
    # TODO: llamar a guardar_notas() y avisar el resultado en txt_estado
    pass


def main():
    dpg.create_context()

    dpg.create_viewport(title="Dear PyGui - Calificaciones", width=460, height=600)

    dpg.add_window(
        tag="ventana_principal",
        label="Planilla de calificaciones",
        width=440,
        height=560,
    )

    dpg.add_text("Cargá un alumno y su nota:", parent="ventana_principal")
    dpg.add_input_text(tag="input_alumno", label="Alumno", width=300, parent="ventana_principal")
    dpg.add_input_text(tag="input_nota", label="Nota (1 a 10)", width=300, parent="ventana_principal")

    dpg.add_button(label="Agregar nota", callback=al_agregar, parent="ventana_principal")
    dpg.add_button(label="Ver resumen", callback=al_ver_resumen, parent="ventana_principal")
    dpg.add_button(label="Guardar", callback=al_guardar, parent="ventana_principal")

    dpg.add_spacer(height=6, parent="ventana_principal")
    dpg.add_text("", tag="txt_estado", wrap=400, parent="ventana_principal")

    dpg.add_separator(parent="ventana_principal")
    dpg.add_text("Notas cargadas:", parent="ventana_principal")
    dpg.add_child_window(
        tag="panel_notas",
        parent="ventana_principal",
        width=405,
        height=100,
        border=True,
    )
    dpg.add_text("Acá aparecen los alumnos con sus notas...", wrap=370, parent="panel_notas")

    dpg.add_text("Resumen:", parent="ventana_principal")
    dpg.add_input_text(
        tag="txt_resumen",
        multiline=True,
        readonly=True,
        width=405,
        height=160,
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