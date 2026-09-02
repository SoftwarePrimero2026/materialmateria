"""Lógica de negocio del control de gastos.

Capa intermedia entre la interfaz y la base de datos: valida los datos
del formulario y usa `base_datos` para persistirlos en SQLite.

La interfaz NUNCA toca SQLite: llama a estas funciones y ellas deciden
cuándo y cómo consultar la base.
"""

from modulos import base_datos

# Presupuestos leídos desde la tabla `presupuestos` de SQLite.
# Se cargan una sola vez, al importar este módulo.
PRESUPUESTOS = base_datos.presupuestos()


def _validar_gasto(categoria, monto_texto, descripcion) -> tuple[str, float, str] | str:
    """Valida los datos del formulario.

    Devuelve la tupla (categoria, monto, descripcion) si son válidos, o
    un `str` con el mensaje de error si hay algún problema.
    """
    categoria = categoria.strip().lower()
    descripcion = descripcion.strip()

    try:
        monto = float(monto_texto.strip().replace(",", "."))
    except ValueError:
        return "El monto debe ser un número (ej: 1200)."

    if categoria not in PRESUPUESTOS:
        return f"La categoría '{categoria}' no existe en el presupuesto."
    if monto <= 0:
        return "El monto debe ser mayor a cero."
    if not descripcion:
        return "Escribí una breve descripción del gasto."

    return (categoria, monto, descripcion)


def agregar_gasto(categoria, monto_texto, descripcion):
    """Valida y registra un gasto. Alerta si se supera el presupuesto.

    Devuelve (ok, mensaje). El mensaje puede incluir la alerta de
    exceso de presupuesto aunque el gasto se haya registrado.
    """
    datos = _validar_gasto(categoria, monto_texto, descripcion)
    if isinstance(datos, str):
        return False, datos
    categoria, monto, descripcion = datos

    base_datos.insertar_gasto(categoria, monto, descripcion)

    total_categoria = total_por_categoria(categoria)
    presupuesto = PRESUPUESTOS[categoria]
    if total_categoria > presupuesto:
        exceso = total_categoria - presupuesto
        return True, (
            f"Gasto registrado. ¡Atención! Te pasaste del presupuesto de "
            f"{categoria} por ${exceso:,.2f}."
        )

    return True, "Gasto registrado correctamente."


def listar_gastos():
    """Devuelve todas las filas de gastos para mostrar en la tabla."""
    return base_datos.listar_gastos()


def obtener_gasto(id_gasto):
    """Devuelve un gasto por id (para cargarlo en el formulario)."""
    return base_datos.obtener_gasto(id_gasto)


def actualizar_gasto(id_gasto, categoria, monto_texto, descripcion):
    """Valida y modifica un gasto existente.

    Devuelve (ok, mensaje). La validación es la misma que al agregar.
    """
    datos = _validar_gasto(categoria, monto_texto, descripcion)
    if isinstance(datos, str):
        return False, datos
    categoria, monto, descripcion = datos

    if base_datos.actualizar_gasto(id_gasto, categoria, monto, descripcion) == 0:
        return False, "No se encontró un gasto con ese id."

    total_categoria = total_por_categoria(categoria)
    presupuesto = PRESUPUESTOS[categoria]
    if total_categoria > presupuesto:
        exceso = total_categoria - presupuesto
        return True, (
            f"Gasto actualizado. ¡Atención! Te pasaste del presupuesto de "
            f"{categoria} por ${exceso:,.2f}."
        )

    return True, "Gasto actualizado correctamente."


def eliminar_gasto(id_gasto):
    """Borra un gasto por id.

    Devuelve (ok, mensaje).
    """
    if base_datos.eliminar_gasto(id_gasto) == 0:
        return False, "No se encontró un gasto con ese id."

    return True, "Gasto eliminado correctamente."


def total_por_categoria(categoria):
    """Suma todos los gastos de una categoría (consulta a SQLite)."""
    return base_datos.total_por_categoria(categoria)


def total_general():
    """Suma todos los gastos del mes (consulta a SQLite)."""
    return base_datos.total_general()


def categorias_con_exceso():
    """Devuelve {categoria: monto_excedido} para las que pasaron el presupuesto."""
    excesos = {}
    for categoria, presupuesto in PRESUPUESTOS.items():
        gastado = total_por_categoria(categoria)
        if gastado > presupuesto:
            excesos[categoria] = gastado - presupuesto
    return excesos


def resumen_general():
    """Arma el resumen por categorías con presupuesto, gastado y restante."""
    ancho_categoria = 12
    ancho_monto = 14  # "$ 50,000.00" entra holgado en 14 columnas

    texto = "=========== RESUMEN GENERAL ===========\n"
    texto += (
        f"{'Categoría':<{ancho_categoria}}"
        f"{'Presupuesto':>{ancho_monto}}"
        f"{'Gastado':>{ancho_monto}}"
        f"{'Restante':>{ancho_monto}}\n"
    )
    texto += "-" * (ancho_categoria + ancho_monto * 3) + "\n"

    for categoria, presupuesto in PRESUPUESTOS.items():
        gastado = total_por_categoria(categoria)
        restante = presupuesto - gastado
        texto += (
            f"{categoria:<{ancho_categoria}}"
            f"${presupuesto:>{ancho_monto - 1},.2f}"
            f"${gastado:>{ancho_monto - 1},.2f}"
            f"${restante:>{ancho_monto - 1},.2f}\n"
        )

    texto += "-" * (ancho_categoria + ancho_monto * 3) + "\n"
    texto += (
        f"{'TOTAL':<{ancho_categoria}}"
        f"{'':>{ancho_monto}}"
        f"${total_general():>{ancho_monto - 1},.2f}\n"
    )

    excesos = categorias_con_exceso()
    if excesos:
        texto += "\n¡ATENCIÓN! Superaste el presupuesto de:\n"
        for categoria, exceso in excesos.items():
            texto += f"  · {categoria} (te pasaste por ${exceso:,.2f})\n"
    else:
        texto += "\nNo superaste ningún presupuesto."

    texto += "=" * (ancho_categoria + ancho_monto * 3)
    return texto