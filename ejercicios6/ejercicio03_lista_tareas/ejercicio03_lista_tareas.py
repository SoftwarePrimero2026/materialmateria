"""Ejercicio 3 - Lista de tareas con estados y guardado.

La ventana inicial ya está armada. Tu tarea:
  1. Creá el módulo `modulos/servicio_tareas.py` con la lógica
     (carga del archivo, alta, avance de estado, eliminación, listado,
     guardado) y las funciones del enunciado.
  2. Completá los callbacks para conectar los botones con el módulo.
"""

from dearpygui import dearpygui as dpg

# TODO: importar las funciones de la lógica
# from modulos.servicio_tareas import (
#     cargar_tareas, agregar_tarea, avanzar_estado, eliminar_tarea,
#     listado_tareas, guardar_tareas,
# )


def refrescar_panel():
    """Redibuja el panel con las tareas agrupadas por estado."""
    # TODO: borrar los hijos del panel_tareas y dibujar listado_tareas()
    pass


def al_agregar():
    """Toma la descripción y el estado del combo, y agrega la tarea."""
    # TODO: leer input_tarea / combo_estado -> agregar_tarea()
    pass


def al_avanzar():
    # TODO: leer input_tarea -> avanzar_estado()
    pass


def al_eliminar():
    # TODO: leer input_tarea -> eliminar_tarea()
    pass


def al_guardar():
    # TODO: llamar a guardar_tareas() y avisar el resultado en txt_estado
    pass


def main():
    dpg.create_context()

    dpg.create_viewport(title="Dear PyGui - Lista de tareas", width=460, height=600)

    dpg.add_window(
        tag="ventana_principal",
        label="Lista de tareas",
        width=440,
        height=560,
    )

    dpg.add_text("Descripción de la tarea:", parent="ventana_principal")
    dpg.add_input_text(tag="input_tarea", label="Tarea", width=300, parent="ventana_principal")
    dpg.add_combo(
        tag="combo_estado",
        items=["pendiente", "en curso", "completada"],
        label="Estado",
        default_value="pendiente",
        width=260,
        parent="ventana_principal",
    )

    dpg.add_button(label="Agregar tarea", callback=al_agregar, parent="ventana_principal")
    dpg.add_button(label="Avanzar estado", callback=al_avanzar, parent="ventana_principal")
    dpg.add_button(label="Eliminar tarea", callback=al_eliminar, parent="ventana_principal")
    dpg.add_button(label="Guardar", callback=al_guardar, parent="ventana_principal")

    dpg.add_spacer(height=6, parent="ventana_principal")
    dpg.add_text("", tag="txt_estado", wrap=400, parent="ventana_principal")

    dpg.add_separator(parent="ventana_principal")
    dpg.add_text("Mis tareas:", parent="ventana_principal")
    dpg.add_child_window(
        tag="panel_tareas",
        parent="ventana_principal",
        width=405,
        height=260,
        border=True,
    )
    dpg.add_text("Acá aparecen tus tareas agrupadas por estado...", wrap=370, parent="panel_tareas")

    dpg.setup_dearpygui()
    dpg.set_primary_window("ventana_principal", True)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()