# =====================================================================
# Ejercicio 2 — Sistema de turnos de una peluquería
# Solución de referencia (para corrección)
# Conceptos: diccionarios, ciclos, decisiones, funciones, recorridos,
#            cálculo de porcentajes, manejo de entradas inválidas.
# =====================================================================

# Horarios fijos en los que atiende la peluquería.
HORARIOS = ["09:00", "10:00", "11:00", "12:00", "16:00", "17:00", "18:00"]

# Valor que usamos para indicar que un horario está libre.
LIBRE = "libre"


def crear_agenda():
    """Crea el diccionario inicial: cada horario empieza 'libre'."""
    agenda = {}
    for horario in HORARIOS:
        agenda[horario] = LIBRE
    return agenda


def ver_agenda(agenda):
    """Muestra todos los horarios con su estado actual."""
    print("\n--- AGENDA DEL DÍA ---")
    for horario in HORARIOS:  # recorremos en orden de horario
        cliente = agenda[horario]
        if cliente == LIBRE:
            print(f"{horario}  ->  LIBRE")
        else:
            print(f"{horario}  ->  {cliente}")


def horarios_libres(agenda):
    """Devuelve una lista con los horarios que están libres."""
    libres = []
    for horario in HORARIOS:
        if agenda[horario] == LIBRE:
            libres.append(horario)
    return libres


def reservar(agenda):
    """Reserva un turno libre para un cliente."""
    libres = horarios_libres(agenda)
    if len(libres) == 0:
        print("No hay horarios libres.")
        return

    print(f"Horarios libres: {', '.join(libres)}")
    horario = input("Ingrese el horario a reservar: ")

    # Validamos que el horario exista y esté libre.
    if horario not in agenda:
        print("Ese horario no existe.")
    elif agenda[horario] != LIBRE:
        print("Ese horario ya está ocupado.")
    else:
        nombre = input("Nombre del cliente: ").strip()
        # Un cliente no puede tener dos turnos el mismo día.
        if nombre in agenda.values():
            print(f"{nombre} ya tiene un turno reservado.")
        else:
            agenda[horario] = nombre
            print(f"Turno reservado para {nombre} a las {horario}.")


def cancelar(agenda):
    """Libera un horario reservado."""
    horario = input("Ingrese el horario a cancelar: ")
    if horario not in agenda:
        print("Ese horario no existe.")
    elif agenda[horario] == LIBRE:
        print("Ese horario ya estaba libre, no hay nada que cancelar.")
    else:
        cliente = agenda[horario]
        agenda[horario] = LIBRE
        print(f"Turno de {cliente} a las {horario} cancelado.")


def buscar_cliente(agenda):
    """Busca en qué horario tiene turno un cliente."""
    nombre = input("Nombre del cliente a buscar: ").strip()
    encontrado = False
    for horario in HORARIOS:
        if agenda[horario] == nombre:
            print(f"{nombre} tiene turno a las {horario}.")
            encontrado = True
    if not encontrado:
        print(f"{nombre} no tiene ningún turno reservado.")


def ver_resumen(agenda):
    """Muestra reservados, libres y porcentaje de ocupación."""
    total = len(HORARIOS)
    reservados = 0
    for horario in HORARIOS:
        if agenda[horario] != LIBRE:
            reservados += 1
    libres = total - reservados
    porcentaje = reservados / total * 100

    print("\n--- RESUMEN DEL DÍA ---")
    print(f"Turnos reservados: {reservados}")
    print(f"Turnos libres:     {libres}")
    print(f"Ocupación:         {porcentaje:.1f}%")


def mostrar_menu():
    print("\n===== TURNOS PELUQUERÍA =====")
    print("1. Ver agenda")
    print("2. Reservar turno")
    print("3. Cancelar turno")
    print("4. Buscar turno de un cliente")
    print("5. Ver resumen del día")
    print("6. Salir")


def main():
    agenda = crear_agenda()  # arranca con todos los horarios libres

    while True:
        mostrar_menu()
        opcion = input("Elija una opción: ")

        if opcion == "1":
            ver_agenda(agenda)
        elif opcion == "2":
            reservar(agenda)
        elif opcion == "3":
            cancelar(agenda)
        elif opcion == "4":
            buscar_cliente(agenda)
        elif opcion == "5":
            ver_resumen(agenda)
        elif opcion == "6":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


main()
