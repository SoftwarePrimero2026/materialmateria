"""Funciones de procesamiento usadas por los callbacks de la UI."""


def normalizar_nombre(nombre):
    """Limpia espacios y transforma el texto."""
    return " ".join(nombre.strip().split()).title()


def construir_mensaje_bienvenida(nombre):
    """Devuelve un mensaje listo para mostrarse en un widget de texto."""
    nombre_limpio = normalizar_nombre(nombre)
    if not nombre_limpio:
        return "Escribe un nombre antes de presionar el botón."
    return f"Hola, {nombre_limpio}. El texto fue procesado en otro módulo."
