from dearpygui import dearpygui as dpg
from modulos.servicio_auth import validar_login as validar_pin

# Variables de Contexto del Viewport
VIEWPORT_WIDTH = 600
VIEWPORT_HEIGHT = 400
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
TOP_X = 100
TOP_Y = 50
LOGIN_FRAME_WIDTH = 220
LOGIN_FRAME_HEIGHT = 150
MENU_FRAME_WIDTH = 550
MENU_FRAME_HEIGHT = 350

ESPACIO_HORIZONTAL = 15
ESPACIO_VERTICAL = 10

# Configuración de los elementos de la ventana principal
label = {
    "size": {"width": 150, "height": 80},
    "pos": {"x": 0, "y": 10},
}
boton_izq_1_config = {
    "size": {"width": 50, "height": 30},
    "pos": {"x": 10, "y": 10},
}
boton_izq_2_config = {
    "size": {"width": 50, "height": 30},
    "pos": {"x": 10, "y": 0},
}
boton_der_1_config = {
    "size": {"width": 50, "height": 30},
    "pos": {"x": 0, "y": 10},
}
boton_der_2_config = {
    "size": {"width": 50, "height": 30},
    "pos": {"x": 0, "y": 0},
}

label["pos"]["x"] = (
    boton_izq_1_config["pos"]["x"]
    + boton_izq_1_config["size"]["width"]
    + ESPACIO_HORIZONTAL
)

boton_izq_2_config["pos"]["y"] = (
    boton_izq_1_config["pos"]["y"]
    + boton_izq_1_config["size"]["height"]
    + ESPACIO_VERTICAL
)

boton_der_1_config["pos"]["x"] = (
    label["pos"]["x"]
    + label["size"]["width"]
    + ESPACIO_HORIZONTAL
)
boton_der_2_config["pos"]["x"] = boton_der_1_config["pos"]["x"]
boton_der_2_config["pos"]["y"] = boton_izq_2_config["pos"]["y"]

def intentar_ingreso():
    """Valida credenciales y cambia de ventana cuando es correcto."""
    pin = dpg.get_value("login_pin")

    ok, mensaje = validar_pin(pin)  # Usando "admin" como usuario fijo para el demo
    dpg.set_value("login_estado", mensaje)

    if ok:
        dpg.hide_item("pantalla")
        dpg.show_item("ventana_menu")

def cerrar_sesion():
    """Vuelve al formulario de login y limpia los campos."""
    dpg.set_value("login_pin", "")
    dpg.set_value("login_estado", "Sesión cerrada.")

    dpg.hide_item("ventana_menu")
    dpg.show_item("pantalla")


def escribir_mensaje(mensaje):
    """Escribe un mensaje en el label central."""
    dpg.set_value("label_central", mensaje)


# Callbacks de los 4 botones.
def boton_izq_1():
    escribir_mensaje("Mensaje desde Izq 1")


def boton_izq_2():
    escribir_mensaje("Mensaje desde Izq 2")


def boton_der_1():
    escribir_mensaje("Mensaje desde Der 1")


def main():
    dpg.create_context()

    dpg.create_viewport(title='Cajero GUI',
                        x_pos=SCREEN_WIDTH+TOP_X,
                        y_pos=TOP_Y,
                        width=VIEWPORT_WIDTH,
                        height=VIEWPORT_HEIGHT,
                        resizable=False,
                        max_width=VIEWPORT_WIDTH,
                        max_height=VIEWPORT_HEIGHT,
                        min_width=VIEWPORT_WIDTH,
                        min_height=VIEWPORT_HEIGHT)

    dpg.add_window(tag="pantalla",
                   label="Ingreso de PIN",
                   width=VIEWPORT_WIDTH,
                   height=VIEWPORT_HEIGHT,
                   no_resize=True,
                   no_collapse=True,
                   no_close=True)

    marco_x = (VIEWPORT_WIDTH - LOGIN_FRAME_WIDTH) // 2
    marco_y = (VIEWPORT_HEIGHT - LOGIN_FRAME_HEIGHT) // 2

    dpg.add_child_window(tag="marco_login",
                         parent="pantalla",
                         width=LOGIN_FRAME_WIDTH,
                         height=LOGIN_FRAME_HEIGHT,
                         pos=(marco_x, marco_y),
                         border=True,
                         no_scrollbar=True)
    dpg.add_spacer(parent="marco_login", height=12)
    dpg.add_text("Ingrese Su Codigo PIN:", parent="marco_login")
    dpg.add_spacer(parent="marco_login", height=8)
    dpg.add_input_text(tag="login_pin", parent="marco_login", password=True, width=200)
    dpg.add_spacer(parent="marco_login", height=8)
    dpg.add_button(label="Ingresar", parent="marco_login", callback=intentar_ingreso, width=200)
    dpg.add_spacer(parent="marco_login", height=6)
    dpg.add_text("", tag="login_estado", parent="marco_login")

    dpg.add_window(tag="ventana_menu",
                   label="Menu Principal",
                   width=VIEWPORT_WIDTH,
                   height=VIEWPORT_HEIGHT,
                   show=False,
                   no_resize=True,
                   no_collapse=True,
                   no_close=True)

    marco_x_menu = (VIEWPORT_WIDTH - MENU_FRAME_WIDTH) // 2
    marco_y_menu = (VIEWPORT_HEIGHT - MENU_FRAME_HEIGHT) // 2

    dpg.add_child_window(tag="marco_menu",
                         parent="ventana_menu",
                         width=MENU_FRAME_WIDTH,
                         height=MENU_FRAME_HEIGHT,
                         pos=(marco_x_menu, marco_y_menu),
                         border=True)

    # Botones izquierdos
    dpg.add_button(
        label="I1",
        parent="marco_menu",
        width=boton_izq_1_config["size"]["width"],
        height=boton_izq_1_config["size"]["height"],
        pos=(boton_izq_1_config["pos"]["x"], boton_izq_1_config["pos"]["y"]),
        callback=boton_izq_1,
    )
    dpg.add_button(
        label="I2",
        parent="marco_menu",
        width=boton_izq_2_config["size"]["width"],
        height=boton_izq_2_config["size"]["height"],
        pos=(boton_izq_2_config["pos"]["x"], boton_izq_2_config["pos"]["y"]),
        callback=boton_izq_2,
    )

    # Botones derechos
    dpg.add_button(
        label="D1",
        parent="marco_menu",
        width=boton_der_1_config["size"]["width"],
        height=boton_der_1_config["size"]["height"],
        pos=(boton_der_1_config["pos"]["x"], boton_der_1_config["pos"]["y"]),
        callback=boton_der_1,
    )
    dpg.add_button(
        label="SALIR",
        parent="marco_menu",
        width=boton_der_2_config["size"]["width"],
        height=boton_der_2_config["size"]["height"],
        pos=(boton_der_2_config["pos"]["x"], boton_der_2_config["pos"]["y"]),
        callback=cerrar_sesion,
    )

    dpg.add_child_window(tag="marco_label",
                         parent="marco_menu",
                         width=label["size"]["width"],
                         height=label["size"]["height"],
                         pos=(label["pos"]["x"], label["pos"]["y"]),
                         border=True)
    dpg.add_text(
        "Esperando mensaje...",
        tag="label_central",
        parent="marco_label",
        wrap=label["size"]["width"] - 10,
    )

    dpg.setup_dearpygui()
    dpg.set_primary_window("pantalla", True)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
