"""Servicio simple de autenticación para demos."""


USUARIOS_DEMO = {
    "admin": "1234",
    "alumno": "python",
}


def validar_login(usuario, clave):
    """Valida credenciales y devuelve (ok, mensaje)."""
    usuario = usuario.strip().lower()
    clave = clave.strip()

    if not usuario or not clave:
        return False, "Completa usuario y contraseña."

    clave_esperada = USUARIOS_DEMO.get(usuario)
    if clave_esperada is None:
        return False, "Usuario no encontrado."

    if clave != clave_esperada:
        return False, "Contraseña incorrecta."

    return True, f"Bienvenido/a, {usuario}."
