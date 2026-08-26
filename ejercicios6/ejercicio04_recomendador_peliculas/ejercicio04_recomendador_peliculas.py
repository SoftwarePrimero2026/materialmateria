"""Ejercicio 4 - Recomendador de películas con catálogo en archivo.

La ventana inicial ya está armada. Tu tarea:
  1. Creá el módulo `modulos/servicio_peliculas.py` con la lógica
     (carga del catálogo y de las vistas, alta, marcar vista, recomendación,
     guardado) y las funciones del enunciado.
  2. Completá los callbacks para conectar los botones con el módulo.
"""

from dearpygui import dearpygui as dpg

# TODO: importar las funciones de la lógica
# from modulos.servicio_peliculas import (
#     cargar_datos, agregar_pelicula, marcar_vista, recomendar,
#     catalogo_texto, guardar_datos,
# )


def refrescar_panel():
    """Redibuja el panel con el catálogo agrupado por género."""
    # TODO: borrar los hijos del panel_catalogo y dibujar catalogo_texto()
    pass


def al_agregar():
    """Toma título y género, y agrega la película al catálogo."""
    # TODO: leer input_titulo / input_genero -> agregar_pelicula()
    pass


def al_marcar_vista():
    # TODO: leer input_titulo -> marcar_vista()
    pass


def al_recomendar():
    # TODO: leer input_genero -> recomendar() y mostrarlo en txt_recomendacion
    pass


def al_guardar():
    # TODO: llamar a guardar_datos() y avisar el resultado en txt_estado
    pass


def main():
    dpg.create_context()

    dpg.create_viewport(title="Dear PyGui - Recomendador de películas", width=480, height=640)

    dpg.add_window(
        tag="ventana_principal",
        label="Recomendador de películas",
        width=460,
        height=600,
    )

    dpg.add_text("Título y género:", parent="ventana_principal")
    dpg.add_input_text(tag="input_titulo", label="Título", width=320, parent="ventana_principal")
    dpg.add_input_text(tag="input_genero", label="Género", width=320, parent="ventana_principal")

    dpg.add_button(label="Agregar película", callback=al_agregar, parent="ventana_principal")
    dpg.add_button(label="Marcar como vista", callback=al_marcar_vista, parent="ventana_principal")
    dpg.add_button(label="Recomendar", callback=al_recomendar, parent="ventana_principal")
    dpg.add_button(label="Guardar", callback=al_guardar, parent="ventana_principal")

    dpg.add_spacer(height=6, parent="ventana_principal")
    dpg.add_text("", tag="txt_estado", wrap=420, parent="ventana_principal")

    dpg.add_separator(parent="ventana_principal")
    dpg.add_text("Catálogo:", parent="ventana_principal")
    dpg.add_child_window(
        tag="panel_catalogo",
        parent="ventana_principal",
        width=425,
        height=170,
        border=True,
    )
    dpg.add_text("Acá aparece tu catálogo agrupado por género...", wrap=390, parent="panel_catalogo")

    dpg.add_text("Recomendación:", parent="ventana_principal")
    dpg.add_input_text(
        tag="txt_recomendacion",
        multiline=True,
        readonly=True,
        width=425,
        height=110,
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