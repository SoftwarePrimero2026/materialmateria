"""Ejercicio 3 - Agenda de contactos con inicio de sesión.

Combina el patrón de login con cambio de ventana (como el ejemplo_02)
con la lógica de la agenda del TP 2.
"""

from dearpygui import dearpygui as dpg

from modulos.servicio_agenda import (
    agregar_contacto,
    buscar_contacto,
    eliminar_contacto,
    listar_contactos,
)
from modulos.servicio_auth import validar_login


# ------------------------- Login -------------------------

def intentar_login():
    """Valida las credenciales y, si son correctas, cambia de ventana."""
    usuario = dpg.get_value("login_usuario")
    clave = dpg.get_value("login_clave")

    ok, mensaje = validar_login(usuario, clave)
    dpg.set_value("login_estado", mensaje)

    if ok:
        dpg.set_value("txt_saludo", mensaje)
        dpg.hide_item("ventana_login")
        dpg.show_item("ventana_agenda")


# ------------------------- Agenda -------------------------

def actualizar_paneles():
    """Refresca la tabla de contactos de la ventana."""
    dpg.delete_item("panel_contactos", children_only=True)
    dpg.add_text(listar_contactos(), parent="panel_contactos", wrap=420)


def al_agregar_contacto():
    ok, mensaje = agregar_contacto(
        dpg.get_value("input_nuevo_nombre"),
        dpg.get_value("input_nuevo_telefono"),
        dpg.get_value("input_nuevo_correo"),
    )
    dpg.set_value("txt_estado_agenda", mensaje)

    if ok:
        dpg.set_value("input_nuevo_nombre", "")
        dpg.set_value("input_nuevo_telefono", "")
        dpg.set_value("input_nuevo_correo", "")
        actualizar_paneles()


def al_buscar_contacto():
    ok, mensaje, datos = buscar_contacto(dpg.get_value("input_buscar"))
    if ok and datos is not None:
        nombre, telefono, correo = datos
        mensaje = f"{nombre} → {telefono} | {correo}"
    dpg.set_value("txt_resultado_busqueda", mensaje)


def al_eliminar_contacto():
    ok, mensaje = eliminar_contacto(dpg.get_value("input_eliminar"))
    dpg.set_value("txt_estado_agenda", mensaje)
    if ok:
        dpg.set_value("input_eliminar", "")
        actualizar_paneles()


def cerrar_sesion():
    """Limpia el login y vuelve a la ventana de inicio."""
    dpg.set_value("login_usuario", "")
    dpg.set_value("login_clave", "")
    dpg.set_value("login_estado", "Sesión cerrada.")

    dpg.hide_item("ventana_agenda")
    dpg.show_item("ventana_login")


def main():
    dpg.create_context()

    dpg.create_viewport(title="Dear PyGui - Agenda de contactos", width=540, height=600)

    # Ventana de login
    dpg.add_window(
        tag="ventana_login",
        label="Iniciar sesión",
        width=420,
        height=240,
        pos=(20, 20),
    )
    dpg.add_text("Usuarios de prueba: admin / 1234  o  alumno / python", parent="ventana_login")
    dpg.add_input_text(tag="login_usuario", label="Usuario", width=240, parent="ventana_login")
    dpg.add_input_text(tag="login_clave", label="Contraseña", password=True, width=240, parent="ventana_login")
    dpg.add_button(label="Ingresar", callback=intentar_login, parent="ventana_login")
    dpg.add_spacer(height=6, parent="ventana_login")
    dpg.add_text("", tag="login_estado", wrap=380, parent="ventana_login")

    # Ventana de la agenda (oculta hasta loguear)
    dpg.add_window(
        tag="ventana_agenda",
        label="Agenda de contactos",
        width=500,
        height=560,
        pos=(20, 20),
        show=False,
    )
    dpg.add_text("", tag="txt_saludo", parent="ventana_agenda")

    dpg.add_separator(parent="ventana_agenda")
    dpg.add_text("Agregar contacto:", parent="ventana_agenda")
    dpg.add_input_text(tag="input_nuevo_nombre", label="Nombre", width=260, parent="ventana_agenda")
    dpg.add_input_text(tag="input_nuevo_telefono", label="Teléfono", width=260, parent="ventana_agenda")
    dpg.add_input_text(tag="input_nuevo_correo", label="Correo", width=260, parent="ventana_agenda")
    dpg.add_button(label="Agregar", callback=al_agregar_contacto, parent="ventana_agenda")

    dpg.add_separator(parent="ventana_agenda")
    dpg.add_text("Buscar / eliminar:", parent="ventana_agenda")
    dpg.add_input_text(tag="input_buscar", label="Buscar nombre", width=260, parent="ventana_agenda")
    dpg.add_button(label="Buscar contacto", callback=al_buscar_contacto, parent="ventana_agenda")
    dpg.add_text("", tag="txt_resultado_busqueda", wrap=400, parent="ventana_agenda")

    dpg.add_input_text(tag="input_eliminar", label="Eliminar nombre", width=260, parent="ventana_agenda")
    dpg.add_button(label="Eliminar contacto", callback=al_eliminar_contacto, parent="ventana_agenda")

    dpg.add_spacer(height=6, parent="ventana_agenda")
    dpg.add_text("", tag="txt_estado_agenda", wrap=400, parent="ventana_agenda")

    dpg.add_separator(parent="ventana_agenda")
    dpg.add_text("Todos los contactos:", parent="ventana_agenda")
    dpg.add_child_window(
        tag="panel_contactos",
        parent="ventana_agenda",
        width=470,
        height=140,
        border=True,
    )
    dpg.add_text(listar_contactos(), wrap=420, parent="panel_contactos")

    dpg.add_spacer(height=6, parent="ventana_agenda")
    dpg.add_button(label="Cerrar sesión", callback=cerrar_sesion, parent="ventana_agenda")

    dpg.setup_dearpygui()
    dpg.set_primary_window("ventana_login", True)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
