"""Ejemplo 2: login y cambio de ventana (ocultar/mostrar)."""

import dearpygui.dearpygui as dpg

from modulos.servicio_auth import validar_login


def intentar_login():
    """Valida credenciales y cambia de ventana cuando es correcto."""
    usuario = dpg.get_value("login_usuario")
    clave = dpg.get_value("login_clave")

    ok, mensaje = validar_login(usuario, clave)
    dpg.set_value("login_estado", mensaje)

    if ok:
        dpg.set_value("panel_bienvenida", mensaje)
        dpg.hide_item("ventana_login")
        dpg.show_item("ventana_panel")


def cerrar_sesion():
    """Vuelve al formulario de login y limpia los campos."""
    dpg.set_value("login_usuario", "")
    dpg.set_value("login_clave", "")
    dpg.set_value("login_estado", "Sesión cerrada.")

    dpg.hide_item("ventana_panel")
    dpg.show_item("ventana_login")


def main():
    dpg.create_context()

    with dpg.window(tag="ventana_login", label="Login", width=420, height=240, pos=(20, 20)):
        dpg.add_text("Ingresa con un usuario de prueba:")
        dpg.add_text("admin / 1234  o  alumno / python")
        dpg.add_input_text(tag="login_usuario", label="Usuario", width=220)
        dpg.add_input_text(tag="login_clave", label="Contraseña", password=True, width=220)
        dpg.add_button(label="Ingresar", callback=intentar_login)
        dpg.add_spacer(height=6)
        dpg.add_text("", tag="login_estado")

    with dpg.window(
        tag="ventana_panel",
        label="Panel principal",
        width=420,
        height=220,
        pos=(20, 20),
        show=False,
    ):
        dpg.add_text("", tag="panel_bienvenida")
        dpg.add_text("Esta ventana se mostró después de un login válido.")
        dpg.add_button(label="Cerrar sesión", callback=cerrar_sesion)

    dpg.create_viewport(title="Dear PyGui - Ejemplo 2", width=480, height=320)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
