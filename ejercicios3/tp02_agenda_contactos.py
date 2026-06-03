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


def agregar_contacto(agenda):
    """Pide los datos y guarda el contacto en el diccionario."""
    nombre = input("Nombre: ").strip()

    if nombre in agenda:
        print("Ese contacto ya existe.")
        return

    telefono = input("Teléfono: ").strip()
    correo = input("Correo: ").strip()
    agenda[nombre] = (telefono, correo)
    print("Contacto agregado correctamente.")


def buscar_contacto(agenda, nombre):
    """Busca un contacto por nombre y muestra sus datos."""
    if nombre in agenda:
        telefono, correo = agenda[nombre]
        print(f"Nombre: {nombre}")
        print(f"Teléfono: {telefono}")
        print(f"Correo: {correo}")
    else:
        print("No se encontro ese contacto.")


def eliminar_contacto(agenda):
    """Pide un nombre y lo elimina si existe."""
    nombre = input("Nombre a eliminar: ").strip()

    if nombre in agenda:
        del agenda[nombre]
        print("Contacto eliminado.")
    else:
        print("No se encontro ese contacto.")


def listar_contactos(agenda):
    """Imprime todos los contactos en columnas alineadas."""
    if not agenda:
        print("Todavia no hay contactos cargados.")
        return

    print("\n=========== AGENDA DE CONTACTOS ===========")
    print(f"{'Nombre':<20}{'Teléfono':<16}{'Correo'}")
    print("-------------------------------------------")

    for nombre, datos in sorted(agenda.items()):
        telefono, correo = datos
        print(f"{nombre:<20}{telefono:<16}{correo}")

    print("===========================================")
    print(f"Total: {len(agenda)} contactos")


def mostrar_menu():
    print("\n1. Agregar contacto")
    print("2. Buscar contacto")
    print("3. Eliminar contacto")
    print("4. Listar contactos")
    print("5. Salir")


def main():
    agenda = {}

    while True:
        mostrar_menu()
        opcion = input("Elegí una opcion: ")

        if opcion == "1":
            agregar_contacto(agenda)
        elif opcion == "2":
            nombre = input("Nombre a buscar: ").strip()
            buscar_contacto(agenda, nombre)
        elif opcion == "3":
            eliminar_contacto(agenda)
        elif opcion == "4":
            listar_contactos(agenda)
        elif opcion == "5":
            break
        else:
            print("Opcion invalida. Probá nuevamente.")


if __name__ == "__main__":
    main()
