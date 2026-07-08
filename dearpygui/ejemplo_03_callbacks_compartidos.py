"""Ejemplo 3: botones simples para cambiar texto y color."""

import dearpygui.dearpygui as dpg


def mostrar_saludo():
    """Muestra un texto de saludo."""
    dpg.set_value("texto_estado", "Hola! Este texto apareció por el botón Saludar.")


def mostrar_aviso():
    """Muestra un texto de aviso."""
    dpg.set_value("texto_estado", "Atención: este mensaje lo puso el botón Avisar.")


def limpiar_texto():
    """Limpia el texto mostrado."""
    dpg.set_value("texto_estado", "")


def main():
    dpg.create_context()

    with dpg.window(label="Ejemplo 3 - Botones y texto", width=560, height=260):
        dpg.add_text("Presiona un botón para cambiar el texto:")
        dpg.add_button(label="Saludar", callback=mostrar_saludo)
        dpg.add_button(label="Avisar", callback=mostrar_aviso)
        dpg.add_button(label="Limpiar", callback=limpiar_texto)
        dpg.add_spacer(height=8)
        dpg.add_text("", tag="texto_estado", wrap=500)

    dpg.create_viewport(title="Dear PyGui - Ejemplo 3", width=600, height=320)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
