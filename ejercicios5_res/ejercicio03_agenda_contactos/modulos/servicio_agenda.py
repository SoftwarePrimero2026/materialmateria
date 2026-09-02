"""Lógica de la agenda de contactos, separada de la interfaz.

Mantiene el equivalente funcional del TP 2 pero con funciones que
devuelven (ok, mensaje) para que la ventana las muestre fácilmente.
"""

agenda = {}  # { "Ana García": ("011-4523-1234", "ana@mail.com") }


def normalizar_nombre(nombre):
    """Limpia espacios y capitaliza cada palabra del nombre."""
    return " ".join(nombre.strip().split()).title()


def agregar_contacto(nombre, telefono, correo):
    """Guarda un contacto como tupla (telefono, correo) con nombre como clave."""
    nombre = normalizar_nombre(nombre)
    telefono = telefono.strip()
    correo = correo.strip()

    if not nombre:
        return False, "Escribí el nombre del contacto."
    if not telefono or not correo:
        return False, "Completá teléfono y correo."
    if nombre in agenda:
        return False, f"'{nombre}' ya está en la agenda."

    agenda[nombre] = (telefono, correo)
    return True, f"'{nombre}' fue agregado a la agenda."


def buscar_contacto(nombre):
    """Busca un contacto por nombre.

    Devuelve (ok, mensaje, datos) donde datos es (nombre, telefono, correo)
    o None si no se encontró.
    """
    nombre = normalizar_nombre(nombre)

    if not nombre:
        return False, "Escribí un nombre para buscar.", None
    if nombre not in agenda:
        return False, f"'{nombre}' no está en la agenda.", None

    telefono, correo = agenda[nombre]
    return True, "", (nombre, telefono, correo)


def eliminar_contacto(nombre):
    """Elimina un contacto si existe."""
    nombre = normalizar_nombre(nombre)

    if not nombre:
        return False, "Escribí un nombre para eliminar."
    if nombre not in agenda:
        return False, f"'{nombre}' no está en la agenda."

    del agenda[nombre]
    return True, f"'{nombre}' fue eliminado de la agenda."


def listar_contactos():
    """Arma la tabla de contactos alineada en columnas."""
    if not agenda:
        return "La agenda está vacía."

    texto = "=========== AGENDA DE CONTACTOS ===========\n"
    texto += f"{'Nombre':<18}{'Teléfono':<15}Correo\n"
    texto += "-" * 44 + "\n"

    for nombre, (telefono, correo) in sorted(agenda.items()):
        texto += f"{nombre:<18}{telefono:<15}{correo}\n"

    texto += "=" * 44 + f"\nTotal: {len(agenda)} contactos"
    return texto