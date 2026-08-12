"""Ejercicio 3 - Agenda de contactos con inicio de sesión.

Las dos ventanas ya están armadas. Tu tarea:
  1. Creá los módulos `modulos/servicio_auth.py` y `modulos/servicio_agenda.py`
     con la lógica (validación de login y CRUD de contactos).
  2. Completá los callbacks para conectar los widgets con los módulos.
"""

from dearpygui import dearpygui as dpg

# TODO: importar las funciones de la lógica
# from modulos.servicio_auth import validar_login
# from modulos.servicio_agenda import (
#     agregar_contacto, buscar_contacto, eliminar_contacto, listar_contactos,
# )


# ------------------------- Login -------------------------

def intentar_login():
    """Valida las credenciales y, si son correctas, cambia de ventana."""
    # TODO: leer login_usuario / login_clave -> validar_login()
    #       si ok: hide_item("ventana_login"), show_item("ventana_agenda")
    pass


# ------------------------- Agenda -------------------------

def actualizar_paneles():
    """Refresca la tabla de contactos de la ventana."""
    # TODO: borrar hijos del panel_contactos y dibujar listar_contactos()
    pass


def al_agregar_contacto():
    # TODO: leer input_nuevo_* -> agregar_contacto() -> refrescar
    pass


def al_buscar_contacto():
    # TODO: leer input_buscar -> buscar_contacto() -> mostrar en txt_resultado_busqueda
    pass


def al_eliminar_contacto():
    # TODO: leer input_eliminar -> eliminar_contacto() -> refrescar
    pass


def cerrar_sesion():
    # TODO: limpiar login y volver a la ventana de login
    pass


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
    dpg.add_text("Acá va a aparecer la tabla de contactos...", wrap=420, parent="panel_contactos")

    dpg.add_spacer(height=6, parent="ventana_agenda")
    dpg.add_button(label="Cerrar sesión", callback=cerrar_sesion, parent="ventana_agenda")

    dpg.setup_dearpygui()
    dpg.set_primary_window("ventana_login", True)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
