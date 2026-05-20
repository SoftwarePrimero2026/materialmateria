# =============================================================================
# TP 2 — Agenda de contactos
# =============================================================================
#
# ENUNCIADO:
#   Implementar una agenda que almacene nombre, teléfono y correo de
#   contactos. El usuario puede agregar, buscar, eliminar y listar contactos.
#
# ESTRUCTURAS A UTILIZAR:
#   - Diccionario  : clave = nombre del contacto (str).
#   - Tupla        : valor = (teléfono, correo) por cada contacto.
#   - Funciones    : una función por cada operación.
#
# ENTRADA DE DATOS (input):
#   - El usuario ingresa nombre, teléfono y correo al agregar un contacto.
#   - El usuario ingresa el nombre para buscar o eliminar.
#
# SALIDA (print formateado):
#   - La lista de contactos debe mostrarse en columnas alineadas.
#
# EJEMPLO DE SALIDA ESPERADA:
#   =========== AGENDA DE CONTACTOS ===========
#   Nombre              Teléfono        Correo
#   -------------------------------------------
#   Ana García          011-4523-1234   ana@mail.com
#   Carlos Pérez        011-4789-5678   carlos@mail.com
#   ===========================================
#   Total: 2 contactos
#
# INDICACIONES:
#   1. Implementar las funciones:
#        - agregar_contacto(agenda)       → pide datos al usuario y los guarda
#        - buscar_contacto(agenda, nombre)→ muestra los datos de un contacto
#        - eliminar_contacto(agenda)      → pide nombre y lo elimina
#        - listar_contactos(agenda)       → imprime la tabla formateada
#   2. Usar f-strings con especificadores de ancho (:<N) para alinear columnas.
#   3. El nombre se usa como clave; no permitir nombres duplicados.
#   4. Si no existen contactos al listar, mostrar un mensaje informativo.
#
# =============================================================================

# Escribí tu código a partir de aquí:
