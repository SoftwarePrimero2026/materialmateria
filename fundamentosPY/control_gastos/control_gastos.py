"""Ejemplo completo de interfaz gráfica con Dear PyGui y SQLite.

Muestra cómo armar una app de escritorio con CRUD (Crear, Leer,
Actualizar y Eliminar) de gastos, organizada en capas:

  - control_gastos.py        -> interfaz gráfica (Dear PyGui)
  - modulos/servicio_gastos  -> lógica de negocio y validaciones
  - modulos/base_datos       -> acceso a SQLite (solo `sqlite3`, sin ORM)
  - gastos.sql               -> todas las sentencias SQL del proyecto

La interfaz NUNCA habla con SQLite directamente: solo llama a funciones
del módulo de servicio, y este decide cuándo consultar la base.
"""
from dearpygui import dearpygui as dpg

from modulos.servicio_gastos import (
    PRESUPUESTOS,
    actualizar_gasto,
    agregar_gasto,
    eliminar_gasto,
    listar_gastos,
    obtener_gasto,
    resumen_general,
)

# id del gasto que está siendo editado en el formulario.
# None significa "estamos creando un gasto nuevo".
id_en_edicion = None


def refrescar_resumen():
    """Redibuja el panel con el resumen general actualizado."""
    dpg.delete_item("panel_resumen", children_only=True)
    dpg.add_text(resumen_general(), parent="panel_resumen", wrap=430)


# tags de las filas visibles en la tabla, para poder refrescarlas sin
# tocar las columnas. Ojo: `delete_item(children_only=True)` borraría
# las columnas también (son hijas de la tabla) y la tabla quedaría rota.
filas_tabla = []


def refrescar_tabla():
    """Redibuja la tabla con todos los gastos guardados.

    Primero borra solo las filas anteriores (por su tag) y después crea
    una fila por gasto. Cada fila lleva dos botones (Editar / Eliminar)
    que recuerdan el id del gasto a través de `user_data`.
    """
    global filas_tabla
    for fila in filas_tabla:
        dpg.delete_item(fila)
    filas_tabla = []

    for id_gasto, categoria, monto, descripcion, fecha in listar_gastos():
        fila = dpg.add_table_row(parent="tabla_gastos")
        filas_tabla.append(fila)
        dpg.add_text(str(id_gasto), parent=fila)
        dpg.add_text(categoria, parent=fila)
        dpg.add_text(f"${monto:,.2f}", parent=fila)
        dpg.add_text(descripcion, parent=fila)
        dpg.add_text(fecha, parent=fila)

        grupo_acciones = dpg.add_group(horizontal=True, parent=fila)
        dpg.add_button(
            label="Editar",
            small=True,
            callback=al_editar,
            user_data=id_gasto,
            parent=grupo_acciones,
        )
        dpg.add_button(
            label="Eliminar",
            small=True,
            callback=al_eliminar,
            user_data=id_gasto,
            parent=grupo_acciones,
        )


def _reset_formulario():
    """Vuelve el formulario al modo "registrar gasto nuevo".

    No toca el texto de estado (`txt_estado`) para no pisar mensajes.
    """
    global id_en_edicion
    id_en_edicion = None
    dpg.configure_item("btn_guardar", label="Registrar gasto")
    dpg.hide_item("btn_cancelar")
    dpg.set_value("input_monto", "")
    dpg.set_value("input_descripcion", "")


def al_guardar():
    """Registra un gasto nuevo o guarda los cambios de uno en edición.

    Decide qué hacer según `id_en_edicion`:
      - None          -> crear (INSERT)
      - tiene un id   -> actualizar (UPDATE)
    """
    if id_en_edicion is None:
        ok, mensaje = agregar_gasto(
            dpg.get_value("combo_categoria"),
            dpg.get_value("input_monto"),
            dpg.get_value("input_descripcion"),
        )
    else:
        ok, mensaje = actualizar_gasto(
            id_en_edicion,
            dpg.get_value("combo_categoria"),
            dpg.get_value("input_monto"),
            dpg.get_value("input_descripcion"),
        )

    dpg.set_value("txt_estado", mensaje)

    if ok:
        _reset_formulario()
        refrescar_resumen()
        refrescar_tabla()


def al_cancelar():
    """Cancela la edición y vuelve al formulario vacío."""
    _reset_formulario()
    dpg.set_value("txt_estado", "Edición cancelada.")


def al_editar(sender, app_data, user_data):
    """Carga el gasto elegido en el formulario para modificarlo.

    `user_data` trae el id del gasto (el que le pasamos en refrescar_tabla).
    """
    global id_en_edicion
    gasto = obtener_gasto(user_data)
    if gasto is None:
        dpg.set_value("txt_estado", "No se encontró el gasto.")
        return

    id_gasto, categoria, monto, descripcion, _ = gasto
    dpg.set_value("combo_categoria", categoria)
    dpg.set_value("input_monto", str(monto))
    dpg.set_value("input_descripcion", descripcion)

    id_en_edicion = id_gasto
    dpg.configure_item("btn_guardar", label="Guardar cambios")
    dpg.show_item("btn_cancelar")
    dpg.set_value(
        "txt_estado",
        f"Editando el gasto #{id_gasto}. Modificá los campos y guardá.",
    )


def al_eliminar(sender, app_data, user_data):
    """Borra un gasto por id y refresca la pantalla."""
    global id_en_edicion
    ok, mensaje = eliminar_gasto(user_data)

    # Si estábamos editando justo ese gasto, salimos del modo edición.
    if ok and id_en_edicion == user_data:
        _reset_formulario()

    dpg.set_value("txt_estado", mensaje)
    if ok:
        refrescar_resumen()
        refrescar_tabla()


def main():
    dpg.create_context()

    dpg.create_viewport(title="Dear PyGui - Control de gastos", width=520, height=740)

    dpg.add_window(
        tag="ventana_principal",
        label="Control de gastos",
        width=500,
        height=700,
    )

    dpg.add_text("Registrar gasto:", parent="ventana_principal")
    dpg.add_combo(
        tag="combo_categoria",
        items=list(PRESUPUESTOS),
        label="Categoría",
        default_value="comida",
        width=300,
        parent="ventana_principal",
    )
    dpg.add_input_text(tag="input_monto", label="Monto ($)", width=300, parent="ventana_principal")
    dpg.add_input_text(tag="input_descripcion", label="Descripción breve", width=300, parent="ventana_principal")

    grupo_botones = dpg.add_group(horizontal=True, parent="ventana_principal")
    dpg.add_button(tag="btn_guardar", label="Registrar gasto", callback=al_guardar, parent=grupo_botones)
    dpg.add_button(tag="btn_cancelar", label="Cancelar edición", callback=al_cancelar, parent=grupo_botones)
    dpg.hide_item("btn_cancelar")

    dpg.add_spacer(height=4, parent="ventana_principal")
    dpg.add_text("", tag="txt_estado", wrap=460, parent="ventana_principal")

    dpg.add_separator(parent="ventana_principal")
    dpg.add_text("Resumen:", parent="ventana_principal")
    dpg.add_child_window(
        tag="panel_resumen",
        parent="ventana_principal",
        width=470,
        height=160,
        border=True,
    )
    dpg.add_text(resumen_general(), wrap=430, parent="panel_resumen")

    dpg.add_separator(parent="ventana_principal")
    dpg.add_text("Gastos registrados:", parent="ventana_principal")
    dpg.add_child_window(
        tag="panel_gastos",
        parent="ventana_principal",
        width=470,
        height=240,
        border=True,
    )
    dpg.add_table(
        tag="tabla_gastos",
        parent="panel_gastos",
        header_row=True,
        borders_outerV=True,
        borders_innerV=True,
        borders_outerH=True,
        borders_innerH=True,
        row_background=True,
        policy=dpg.mvTable_SizingStretchProp,
    )
    dpg.add_table_column(label="ID", width_fixed=True, width=34, parent="tabla_gastos")
    dpg.add_table_column(label="Categoría", parent="tabla_gastos")
    dpg.add_table_column(label="Monto", width_fixed=True, width=85, parent="tabla_gastos")
    dpg.add_table_column(label="Descripción", parent="tabla_gastos")
    dpg.add_table_column(label="Fecha", width_fixed=True, width=120, parent="tabla_gastos")
    dpg.add_table_column(label="Acciones", width_fixed=True, width=150, parent="tabla_gastos")
    refrescar_tabla()

    dpg.setup_dearpygui()
    dpg.set_primary_window("ventana_principal", True)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()