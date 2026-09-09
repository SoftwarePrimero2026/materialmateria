"""Ejercicio 1 - Registro de temperaturas semanales que se guarda (SQLite).

La ventana inicial ya está armada. Tu tarea:
  1. Creá el archivo `temperaturas.sql` con TODAS las sentencias SQL
     (esquema + consultas parametrizadas), siguiendo el patrón de
     `fundamentosPY/control_gastos/gastos.sql`.
  2. Creá el módulo `modulos/base_datos.py` con el acceso a SQLite:
     conexión que ejecuta el esquema y una función por consulta.
  3. Creá el módulo `modulos/servicio_temperaturas.py` con la lógica
     (validaciones, registrar día, listar registros, resumen) y las
     funciones del enunciado.
  4. Completá los callbacks para conectar los botones con el módulo.
"""

from dearpygui import dearpygui as dpg

# TODO: importar las funciones de la lógica
# from modulos.servicio_temperaturas import (
#     registrar_temperatura, listar_registros, resumen_semanal,
# )


def refrescar_panel():
    """Redibuja el panel con los días y temperaturas cargados."""
    # TODO: borrar los hijos del panel_registros y dibujar los registros
    pass


def al_registrar():
    """Toma el día y las temperaturas y las guarda en la base."""
    # TODO: leer input_dia / input_temp_max / input_temp_min
    #       -> registrar_temperatura() -> refrescar_panel()
    pass


def al_ver_resumen():
    # TODO: mostrar resumen_semanal() en el área txt_resumen
    pass


def main():
    dpg.create_context()

    dpg.create_viewport(title="Dear PyGui - Temperaturas semanales", width=460, height=640)

    dpg.add_window(
        tag="ventana_principal",
        label="Registro de temperaturas semanales",
        width=440,
        height=600,
    )

    dpg.add_text("Cargá el día y sus temperaturas:", parent="ventana_principal")
    dpg.add_combo(
        tag="input_dia",
        label="Día",
        items=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"],
        default_value="Lunes",
        width=300,
        parent="ventana_principal",
    )
    dpg.add_input_text(tag="input_temp_max", label="Temperatura máxima", width=300, parent="ventana_principal")
    dpg.add_input_text(tag="input_temp_min", label="Temperatura mínima", width=300, parent="ventana_principal")

    dpg.add_button(label="Registrar día", callback=al_registrar, parent="ventana_principal")
    dpg.add_button(label="Ver resumen", callback=al_ver_resumen, parent="ventana_principal")

    dpg.add_spacer(height=6, parent="ventana_principal")
    dpg.add_text("", tag="txt_estado", wrap=400, parent="ventana_principal")

    dpg.add_separator(parent="ventana_principal")
    dpg.add_text("Días cargados:", parent="ventana_principal")
    dpg.add_child_window(
        tag="panel_registros",
        parent="ventana_principal",
        width=405,
        height=120,
        border=True,
    )
    dpg.add_text("Acá aparecen los días con sus temperaturas...", wrap=370, parent="panel_registros")

    dpg.add_text("Resumen:", parent="ventana_principal")
    dpg.add_input_text(
        tag="txt_resumen",
        multiline=True,
        readonly=True,
        width=405,
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