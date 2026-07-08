"""Ejemplo 1: botón -> función en otro módulo -> actualización de texto."""

import dearpygui.dearpygui as dpg

from modulos.servicio_texto import construir_mensaje_bienvenida


def al_hacer_click():
    """Lee el input, llama al módulo y muestra el resultado."""
    nombre = dpg.get_value("input_nombre")
    mensaje = construir_mensaje_bienvenida(nombre)

    dpg.set_value("txt_resultado", mensaje)


def main():
    dpg.create_context()

    with dpg.window(label="Ejemplo 1 - Botón y texto", width=560, height=260):
        dpg.add_text("Escribe un nombre y presiona el botón.")
        dpg.add_input_text(tag="input_nombre", label="Nombre", width=260)
        dpg.add_button(label="Procesar nombre", callback=al_hacer_click)
        dpg.add_spacer(height=8)
        dpg.add_text(default_value="Esperando acción...", tag="txt_resultado")

    dpg.create_viewport(title="Dear PyGui - Ejemplo 1", width=600, height=320)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
