"""Ejemplo 4: posicionamiento y dimensiones por codigo."""

import dearpygui.dearpygui as dpg


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


def boton_der_2():
    escribir_mensaje("Mensaje desde Der 2")


def main():
    ESPACIO_HORIZONTAL = 15
    ESPACIO_VERTICAL = 10

    viewport = {
        "size": {"width": 300, "height": 100},
        "pos": {"x": 2000, "y": 80},
    }
    window = {
        "size": {"width": 290, "height": 90},
        "pos": {"x": 0, "y": 0},
    }
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

    dpg.create_context()

    # Ventana Principal
    with dpg.window(
        label="Ejemplo 4 - Posicionamiento",
        tag="ventana_principal",
        width=window["size"]["width"],
        height=window["size"]["height"],
        no_resize=True,
        no_move=True,
        no_title_bar=True,
    ):
        # Area central para mostrar mensajes.
        with dpg.child_window(
            width=label["size"]["width"],
            height=label["size"]["height"],
            pos=(label["pos"]["x"], label["pos"]["y"]),
            border=True,
        ):
            dpg.add_text(
                "Esperando mensaje...",
                tag="label_central",
                wrap=label["size"]["width"] - 10,
            )

        # Botones izquierdos
        dpg.add_button(
            label="I1",
            width=boton_izq_1_config["size"]["width"],
            height=boton_izq_1_config["size"]["height"],
            pos=(boton_izq_1_config["pos"]["x"], boton_izq_1_config["pos"]["y"]),
            callback=boton_izq_1,
        )
        dpg.add_button(
            label="I2",
            width=boton_izq_2_config["size"]["width"],
            height=boton_izq_2_config["size"]["height"],
            pos=(boton_izq_2_config["pos"]["x"], boton_izq_2_config["pos"]["y"]),
            callback=boton_izq_2,
        )

        # Botones derechos
        dpg.add_button(
            label="D1",
            width=boton_der_1_config["size"]["width"],
            height=boton_der_1_config["size"]["height"],
            pos=(boton_der_1_config["pos"]["x"], boton_der_1_config["pos"]["y"]),
            callback=boton_der_1,
        )
        dpg.add_button(
            label="D2",
            width=boton_der_2_config["size"]["width"],
            height=boton_der_2_config["size"]["height"],
            pos=(boton_der_2_config["pos"]["x"], boton_der_2_config["pos"]["y"]),
            callback=boton_der_2,
        )

    dpg.create_viewport(
        title="Dear PyGui - Ejemplo 4",
        width=viewport["size"]["width"],
        height=viewport["size"]["height"],
        x_pos=viewport["pos"]["x"],
        y_pos=viewport["pos"]["y"],
        max_width=viewport["size"]["width"],
        max_height=viewport["size"]["height"],
    )
    dpg.setup_dearpygui()
    dpg.set_primary_window("ventana_principal", True)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
