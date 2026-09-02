"""Lógica del control de gastos personales, separada de la interfaz.

Migración del Ejercicio 4 de `ejercicios4/`: presupuesto por categoría,
registro de gastos y alertas cuando se supera el presupuesto.
"""

PRESUPUESTOS = {
    "comida": 50000.0,
    "transporte": 20000.0,
    "ocio": 15000.0,
}

gastos = []  # lista de tuplas (categoria, monto, descripcion)


def agregar_gasto(categoria, monto_texto, descripcion):
    """Valida y registra un gasto. Alerta si se supera el presupuesto.

    Devuelve (ok, mensaje). El mensaje puede incluir la alerta de
    exceso de presupuesto aunque el gasto se haya registrado.
    """
    categoria = categoria.strip().lower()
    descripcion = descripcion.strip()

    try:
        monto = float(monto_texto.strip().replace(",", "."))
    except ValueError:
        return False, "El monto debe ser un número (ej: 1200)."

    if categoria not in PRESUPUESTOS:
        return False, f"La categoría '{categoria}' no existe en el presupuesto."
    if monto <= 0:
        return False, "El monto debe ser mayor a cero."
    if not descripcion:
        return False, "Escribí una breve descripción del gasto."

    gastos.append((categoria, monto, descripcion))

    total_categoria = total_por_categoria(categoria)
    presupuesto = PRESUPUESTOS[categoria]
    if total_categoria > presupuesto:
        exceso = total_categoria - presupuesto
        return True, (
            f"Gasto registrado. ¡Atención! Te pasaste del presupuesto de "
            f"{categoria} por ${exceso:,.2f}."
        )

    return True, "Gasto registrado correctamente."


def total_por_categoria(categoria):
    """Suma todos los gastos de una categoría."""
    return sum(monto for c, monto, _ in gastos if c == categoria)


def total_general():
    """Suma todos los gastos del mes."""
    return sum(monto for _, monto, _ in gastos)


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