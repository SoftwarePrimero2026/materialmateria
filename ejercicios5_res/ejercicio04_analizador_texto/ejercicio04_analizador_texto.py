"""Ejercicio 4 - Analizador de texto con interfaz gráfica.

Migración del TP 7 (analizador de texto) a Dear PyGui.
Se pega un texto en un área multilínea y el análisis aparece en otra.
"""

from dearpygui import dearpygui as dpg

from modulos.servicio_analizador import analizar_texto


def al_analizar():
    """Toma el texto del área de entrada y muestra el informe."""
    texto = dpg.get_value("input_texto")
    dpg.set_value("txt_informe", analizar_texto(texto))


def al_limpiar():
    """Vuelve a dejar las dos áreas en blanco."""
    dpg.set_value("input_texto", "")
    dpg.set_value("txt_informe", "")
    dpg.set_value("txt_estado", "Áreas limpiadas.")


def main():
    dpg.create_context()

    dpg.create_viewport(title="Dear PyGui - Analizador de texto", width=540, height=600)

    dpg.add_window(
        tag="ventana_principal",
        label="Analizador de texto",
        width=520,
        height=560,
    )

    dpg.add_text("Pegá o escribí un texto:", parent="ventana_principal")
    dpg.add_input_text(
        tag="input_texto",
        multiline=True,
        width=490,
        height=200,
        hint="Escribí tu texto acá...",
        parent="ventana_principal",
    )

    dpg.add_button(label="Analizar texto", callback=al_analizar, parent="ventana_principal")
    dpg.add_button(label="Limpiar", callback=al_limpiar, parent="ventana_principal")
    dpg.add_spacer(height=4, parent="ventana_principal")
    dpg.add_text("", tag="txt_estado", wrap=490, parent="ventana_principal")

    dpg.add_separator(parent="ventana_principal")
    dpg.add_text("Resultado:", parent="ventana_principal")
    dpg.add_input_text(
        tag="txt_informe",
        multiline=True,
        readonly=True,
        width=490,
        height=200,
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
